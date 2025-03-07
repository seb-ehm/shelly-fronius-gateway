import os
import threading
import time
import datetime

import requests
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.server import StartTcpServer

from register_mapping import map_values_to_registers
from modbus import initialize_datablock_and_context

import json

MODBUS_PORT = 502
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "shelly_url": "http://shelly/rpc/Shelly.GetStatus",
    "shelly_offsets": {
        "a_total_act_energy": 0,
        "a_total_act_ret_energy": 0,
        "b_total_act_energy": 0,
        "b_total_act_ret_energy": 0,
        "c_total_act_energy": 0,
        "c_total_act_ret_energy": 0,
        "total_act": 0,
        "total_act_ret": 0
    },
    "nullify_channel": []
}

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE) as f:
        config = json.load(f)
else:
    print("⚠️  Warning: No config.json found, using defaults!")
    config = DEFAULT_CONFIG

lock = threading.Lock()

def remove_offsets(data):
    data['emdata:0']["a_total_act_energy"] -= config['offsets']['a_total_act_energy']
    data['emdata:0']["a_total_act_ret_energy"] -= config['offsets']['a_total_act_ret_energy']
    data['emdata:0']["b_total_act_energy"] -= config['offsets']['b_total_act_energy']
    data['emdata:0']["b_total_act_ret_energy"] -= config['offsets']['b_total_act_ret_energy']
    data['emdata:0']["c_total_act_energy"] -= config['offsets']['c_total_act_energy']
    data['emdata:0']["c_total_act_ret_energy"] -= config['offsets']['c_total_act_ret_energy']
    data['emdata:0']["total_act"] -= config['offsets']['total_act']
    data['emdata:0']["total_act_ret"] -= config['offsets']['total_act_ret']
    return data

def nullify_channel(data):
    """Remove data from a shelly channel, if it is not used by an inverter"""
    # Validate the channel parameter
    for channel in config['nullify_channel']:
        if channel not in ['a', 'b', 'c']:
            raise ValueError("Channel must be 'a', 'b', or 'c'.")

        # Nullify the specified channel in 'em:0'
        for key in list(data['em:0'].keys()):
            if key.startswith(f'{channel}_') and key not in [f'{channel}_freq', f'{channel}_voltage']:
                data['em:0'][key] = 0 if isinstance(data['em:0'][key], (int, float)) else None

        # Recalculate total values in 'em:0'
        active_channels = [ch for ch in ['a', 'b', 'c'] if ch != channel]
        data['em:0']['total_current'] = sum(data['em:0'][f'{ch}_current'] for ch in active_channels)
        data['em:0']['total_act_power'] = sum(data['em:0'][f'{ch}_act_power'] for ch in active_channels)
        data['em:0']['total_aprt_power'] = sum(data['em:0'][f'{ch}_aprt_power'] for ch in active_channels)

        # Nullify the specified channel in 'emdata:0'
        data['emdata:0'][f'{channel}_total_act_energy'] = 0
        data['emdata:0'][f'{channel}_total_act_ret_energy'] = 0

        # Recalculate total values in 'emdata:0'
        data['emdata:0']['total_act'] = sum(data['emdata:0'][f'{ch}_total_act_energy'] for ch in active_channels)
        data['emdata:0']['total_act_ret'] = sum(data['emdata:0'][f'{ch}_total_act_ret_energy'] for ch in active_channels)


def read_shelly():
    response = requests.get(config['shelly_url'])
    response.raise_for_status()
    data = response.json()
    remove_offsets(data)
    nullify_channel(data)

    #put all em data in the same structure
    for key, value in data['emdata:0'].items():
        data['em:0'][key] = value


    return data['em:0']

def float_to_registers(value):
    """Convert a float to a Modbus registers using BinaryPayloadBuilder."""
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
    builder.add_32bit_float(value)  # Add the float value to the payload
    payload = builder.to_registers()  # Convert the payload to 16-bit registers
    return payload

def update_context(context):
    shelly_data = read_shelly()
    modbus_data = map_values_to_registers(shelly_data)

    registers = [0] * 128
    start_address = 40072
    for address, value in modbus_data.items():
        index = address - start_address
        register_values = float_to_registers(value)
        registers[index] = register_values[0]
        registers[index + 1] = register_values[1]
    context[0].setValues(3,72-1, registers)
    return context

def start_modbus_server(context):
    print(f"{datetime.datetime.now()}: ### Starting Modbus server on port {MODBUS_PORT}")
    StartTcpServer(context=context, address=("0.0.0.0", MODBUS_PORT))

def update_data_periodically(context):
    while True:
        update_context(context)
        time.sleep(1)


if __name__ == '__main__':
    datablock, context = initialize_datablock_and_context(lock=lock)
    shelly_thread = threading.Thread(target=update_data_periodically, args=(context,), daemon=True)
    shelly_thread.start()
    start_modbus_server(context)








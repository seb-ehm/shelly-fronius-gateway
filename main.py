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
    data["a_total_act_energy"] -= config['offsets']['a_total_act_energy']
    data["a_total_act_ret_energy"] -= config['offsets']['a_total_act_ret_energy']
    data["b_total_act_energy"] -= config['offsets']['b_total_act_energy']
    data["b_total_act_ret_energy"] -= config['offsets']['b_total_act_ret_energy']
    data["c_total_act_energy"] -= config['offsets']['c_total_act_energy']
    data["c_total_act_ret_energy"] -= config['offsets']['c_total_act_ret_energy']
    data["total_act"] -= config['offsets']['total_act']
    data["total_act_ret"] -= config['offsets']['total_act_ret']
    return data

def nullify_channel(data):
    """Remove data from a shelly channel, if it is not used by an inverter"""
    # Validate the channel parameter
    for channel in config['nullify_channel']:
        if channel not in ['a', 'b', 'c']:
            raise ValueError("Channel must be 'a', 'b', or 'c'.")

        # Nullify the specified channel in 'em:0'
        for key in list(data.keys()):
            if key.startswith(f'{channel}_') and key not in [f'{channel}_freq', f'{channel}_voltage']:
                data[key] = 0 if isinstance(data[key], (int, float)) else None

        # Recalculate total values
        active_channels = [ch for ch in ['a', 'b', 'c'] if ch != channel]
        data['total_current'] = sum(data[f'{ch}_current'] for ch in active_channels)
        data['total_act_power'] = sum(data[f'{ch}_act_power'] for ch in active_channels)
        data['total_aprt_power'] = sum(data[f'{ch}_aprt_power'] for ch in active_channels)

        data['total_act'] = sum(data[f'{ch}_total_act_energy'] for ch in active_channels)
        data['total_act_ret'] = sum(data[f'{ch}_total_act_ret_energy'] for ch in active_channels)


def read_shelly():
    response = requests.get(config['shelly_url'])
    response.raise_for_status()
    data = response.json()
    shelly_data = {**data['em:0'], **data['emdata:0']}
    remove_offsets(shelly_data)
    nullify_channel(shelly_data)

    return shelly_data


def float_to_registers(value):
    """Convert a float to a Modbus registers using BinaryPayloadBuilder."""
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
    builder.add_32bit_float(value)
    payload = builder.to_registers()  # Convert the payload to 16-bit registers
    return payload

def update_context(context):
    shelly_data = read_shelly()
    modbus_data = map_values_to_registers(shelly_data)

    registers = [0] * 128
    start_address = 72
    for address, value in modbus_data.items():
        index = address - start_address
        register_values = float_to_registers(value)
        registers[index] = register_values[0]
        registers[index + 1] = register_values[1]
    context[0].setValues(3,72-1, registers)
    return context

def start_modbus_server(context):
    print(f"{datetime.datetime.now()}: ### Starting Shelly-Fronius-Gateway on port {MODBUS_PORT}")
    StartTcpServer(context=context, address=("0.0.0.0", MODBUS_PORT))

def update_data_periodically(context):
    while True:
        time_to_wait = 1
        try:
            update_context(context)
        except Exception as e:
            print(f"{datetime.datetime.now()}: Failed to update data: {e}")
            time_to_wait = 5 #Sleep a bit longer after an error
        time.sleep(time_to_wait)


if __name__ == '__main__':
    datablock, context = initialize_datablock_and_context(lock=lock)
    shelly_thread = threading.Thread(target=update_data_periodically, args=(context,), daemon=True)
    shelly_thread.start()
    start_modbus_server(context)








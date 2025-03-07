from pymodbus.client import ModbusTcpClient
from pymodbus.client.mixin import ModbusClientMixin
from register_mapping import registers
import struct
import math

# Replace with the actual IP address of your inverter
HOST = "localhost"
PORT = 502  # Default Modbus TCP port
UNIT_ID_INVERTER = 1  # Modbus unit ID for the inverter
UNIT_ID_METER = 200   # Modbus unit ID for the external energy meter

def convert_float32(registers):
    """Convert two 16-bit registers into a 32-bit float."""
    if registers and len(registers) == 2:
        raw = struct.pack(">HH", registers[0], registers[1])  # Big-endian
        return struct.unpack(">f", raw)[0]  # Convert to float
    return None

def convert_int16(value):
    """Convert UInt16 to Int16."""
    return value - 65536 if value > 32767 else value

def read_modbus_register(client, address, length):
    """Read a Modbus register and return the raw data."""
    response = client.read_holding_registers(address-1, count=length, slave=UNIT_ID_INVERTER)
    if response.isError():
        raise Exception(f"Modbus read error: {response}")
    return response.registers


def decode_register(registers, data_type):
    """Decode Modbus register data based on the specified type."""
    if data_type == "uint16":
        return client.convert_from_registers(registers, ModbusClientMixin.DATATYPE.UINT16)
    elif data_type == "uint32":
        return client.convert_from_registers(registers, ModbusClientMixin.DATATYPE.UINT32)
    elif data_type == "float32":
        return client.convert_from_registers(registers, ModbusClientMixin.DATATYPE.FLOAT32)
    elif data_type == "bitfield32":
        # Treat bitfield32 as a uint32 and return the raw value
        raw_value = client.convert_from_registers(registers, ModbusClientMixin.DATATYPE.UINT32)
        # Optionally, you can return a dictionary of bit positions and their values
        bitfield_dict = {i: bool((raw_value >> i) & 1) for i in range(32)}
        return bitfield_dict  # Return either raw_value or bitfield_dict based on your needs
    elif data_type in ["string32", "string16", "string"]:
        # Combine registers into a byte array
        byte_array = bytearray()
        for reg in registers:
            # Split each 16-bit register into two 8-bit bytes (big-endian)
            byte_array.extend(reg.to_bytes(2, byteorder="big"))
        # Decode the byte array into an ASCII string
        string_value = byte_array.decode("ascii").rstrip("\x00")  # Remove null bytes
        return string_value
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

def read_all_registers(client, registers):
    data = {}
    for reg in registers:
        address = reg["address"] # Convert to 0-based index
        length = reg["length"]
        data_type = reg["type"]

        registers_data = read_modbus_register(client, address, length)

        value = decode_register(registers_data, data_type)

        data[reg["name"]] = {"value": value, "description": reg["description"]}
    return data

if __name__ == "__main__":
    client = ModbusTcpClient(HOST, port=PORT)
    client.connect()
    import pprint
    try:
        data = read_all_registers(client, registers)
        pprint.pp(data)
    finally:
        client.close()
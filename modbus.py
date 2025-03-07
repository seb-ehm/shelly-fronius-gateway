from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

class LockedSparseDataBlock(ModbusSparseDataBlock):
    """Thread-safe sparse data block for Modbus."""

    def __init__(self, values, lock):
        super().__init__(values)
        self.lock = lock  # Shared lock for thread safety

    def getValues(self, address, count=1):
        """Ensure thread-safe reads."""
        with self.lock:
            return super().getValues(address, count)

    def setValues(self, address, values):
        """Ensure thread-safe writes."""
        with self.lock:
            return super().setValues(address, values)

def initialize_datablock_and_context(lock):
    # Initialize the data block with initial values
    datablock = LockedSparseDataBlock({
        1: [21365, 28243],
        3: [1],
        4: [65],
        5: [70, 114, 111, 110, 105, 117, 115, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # Manufacturer "Fronius"
            83, 109, 97, 114, 116, 32, 77, 101, 116, 101, 114, 32, 54, 51, 65, 0,  # Device Model "Smart Meter"
            0, 0, 0, 0, 0, 0, 0, 0,  # Options N/A
            0, 0, 0, 0, 0, 0, 0, 0,  # Software Version N/A
            48, 48, 48, 48, 48, 48, 48, 50, 0, 0, 0, 0, 0, 0, 0, 0,  # Serial Number: 00000
            240],  # Modbus TCP Address: 240
        70: [213],
        71: [124],
        72: [0] * 128,  # Initialize address 72 with 128 zeros for payload
        196: [65535, 0],
    }, lock)

    # Create a Modbus slave context
    slave_context = ModbusSlaveContext(
        di=datablock,  # Discrete Inputs
        co=datablock,  # Coils
        hr=datablock,  # Holding Registers
        ir=datablock,  # Input Registers
    )
    context = ModbusServerContext(slaves = slave_context, single = True)
    return datablock, context
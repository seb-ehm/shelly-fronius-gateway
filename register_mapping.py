import math
complete_registers = [
    {"name": "SID", "address": 40001, "length": 2, "type": "uint32", "description": "Well-known value. Uniquely identifies this as a SunSpec Modbus Map"},
    {"name": "ID", "address": 40003, "length": 1, "type": "uint16", "description": "Well-known value. Uniquely identifies this as a SunSpec Common Model block"},
    {"name": "L", "address": 40004, "length": 1, "type": "uint16", "description": "Length of Common Model block"},
    {"name": "Mn", "address": 40005, "length": 16, "type": "string", "description": "Manufacturer"},
    {"name": "Md", "address": 40021, "length": 16, "type": "string", "description": "Device model"},
    {"name": "Opt", "address": 40037, "length": 8, "type": "string", "description": "Options"},
    {"name": "Vr", "address": 40045, "length": 8, "type": "string", "description": "SW version of meter"},
    {"name": "SN", "address": 40053, "length": 16, "type": "string", "description": "Serial number of the meter"},
    {"name": "DA", "address": 40069, "length": 1, "type": "uint16", "description": "Modbus Device Address"},
    {"name": "ID", "address": 40070, "length": 1, "type": "uint16", "description": "Uniquely identifies this as a SunSpec Meter Modbus Map (float); 211: single phase, 212: split phase, 213: three phase"},
    {"name": "L", "address": 40071, "length": 1, "type": "uint16", "description": "Length of inverter model block"},
    {"name": "A", "address": 40072, "length": 2, "type": "float32", "description": "AC Total Current value"},
    {"name": "AphA", "address": 40074, "length": 2, "type": "float32", "description": "AC Phase-A Current value"},
    {"name": "AphB", "address": 40076, "length": 2, "type": "float32", "description": "AC Phase-B Current value"},
    {"name": "AphC", "address": 40078, "length": 2, "type": "float32", "description": "AC Phase-C Current value"},
    {"name": "PhV", "address": 40080, "length": 2, "type": "float32", "description": "AC Voltage Average Phase-to-neutral value"},
    {"name": "PhVphA", "address": 40082, "length": 2, "type": "float32", "description": "AC Voltage Phase-A-to-neutral value"},
    {"name": "PhVphB", "address": 40084, "length": 2, "type": "float32", "description": "AC Voltage Phase-B-to-neutral value"},
    {"name": "PhVphC", "address": 40086, "length": 2, "type": "float32", "description": "AC Voltage Phase-C-to-neutral value"},
    {"name": "PPV", "address": 40088, "length": 2, "type": "float32", "description": "AC Voltage Average Phase-to-phase value"},
    {"name": "PPVphAB", "address": 40090, "length": 2, "type": "float32", "description": "AC Voltage Phase-AB value"},
    {"name": "PPVphBC", "address": 40092, "length": 2, "type": "float32", "description": "AC Voltage Phase-BC value"},
    {"name": "PPVphCA", "address": 40094, "length": 2, "type": "float32", "description": "AC Voltage Phase-CA value"},
    {"name": "Hz", "address": 40096, "length": 2, "type": "float32", "description": "AC Frequency value"},
    {"name": "W", "address": 40098, "length": 2, "type": "float32", "description": "AC Power value"},
    {"name": "WphA", "address": 40100, "length": 2, "type": "float32", "description": "AC Power Phase A value"},
    {"name": "WphB", "address": 40102, "length": 2, "type": "float32", "description": "AC Power Phase B value"},
    {"name": "WphC", "address": 40104, "length": 2, "type": "float32", "description": "AC Power Phase C value"},
    {"name": "VA", "address": 40106, "length": 2, "type": "float32", "description": "AC Apparent Power value"},
    {"name": "VAphA", "address": 40108, "length": 2, "type": "float32", "description": "AC Apparent Power Phase A value"},
    {"name": "VAphB", "address": 40110, "length": 2, "type": "float32", "description": "AC Apparent Power Phase B value"},
    {"name": "VAphC", "address": 40112, "length": 2, "type": "float32", "description": "AC Apparent Power Phase C value"},
    {"name": "VAR", "address": 40114, "length": 2, "type": "float32", "description": "AC Reactive Power value"},
    {"name": "VARphA", "address": 40116, "length": 2, "type": "float32", "description": "AC Reactive Power Phase A value"},
    {"name": "VARphB", "address": 40118, "length": 2, "type": "float32", "description": "AC Reactive Power Phase B value"},
    {"name": "VARphC", "address": 40120, "length": 2, "type": "float32", "description": "AC Reactive Power Phase C value"},
    {"name": "PF", "address": 40122, "length": 2, "type": "float32", "description": "Power Factor value"},
    {"name": "PFphA", "address": 40124, "length": 2, "type": "float32", "description": "Power Factor Phase A value"},
    {"name": "PFphB", "address": 40126, "length": 2, "type": "float32", "description": "Power Factor Phase B value"},
    {"name": "PFphC", "address": 40128, "length": 2, "type": "float32", "description": "Power Factor Phase C value"},
    {"name": "TotWhExp", "address": 40130, "length": 2, "type": "float32", "description": "Total Watt-hours Exported"},
    {"name": "TotWhExpPhA", "address": 40132, "length": 2, "type": "float32", "description": "Total Watt-hours Exported phase A"},
    {"name": "TotWhExpPhB", "address": 40134, "length": 2, "type": "float32", "description": "Total Watt-hours Exported phase B"},
    {"name": "TotWhExpPhC", "address": 40136, "length": 2, "type": "float32", "description": "Total Watt-hours Exported phase C"},
    {"name": "TotWhImp", "address": 40138, "length": 2, "type": "float32", "description": "Total Watt-hours Imported"},
    {"name": "TotWhImpPhA", "address": 40140, "length": 2, "type": "float32", "description": "Total Watt-hours Imported phase A"},
    {"name": "TotWhImpPhB", "address": 40142, "length": 2, "type": "float32", "description": "Total Watt-hours Imported phase B"},
    {"name": "TotWhImpPhC", "address": 40144, "length": 2, "type": "float32", "description": "Total Watt-hours Imported phase C"},
    {"name": "TotVAhExp", "address": 40146, "length": 2, "type": "float32", "description": "Total VA-hours Exported"},
    {"name": "TotVAhExpPhA", "address": 40148, "length": 2, "type": "float32", "description": "Total VA-hours Exported phase A"},
    {"name": "TotVAhExpPhB", "address": 40150, "length": 2, "type": "float32", "description": "Total VA-hours Exported phase B"},
    {"name": "TotVAhExpPhC", "address": 40152, "length": 2, "type": "float32", "description": "Total VA-hours Exported phase C"},
    {"name": "TotVAhImp", "address": 40154, "length": 2, "type": "float32", "description": "Total VA-hours Imported"},
    {"name": "TotVAhImpPhA", "address": 40156, "length": 2, "type": "float32", "description": "Total VA-hours Imported phase A"},
    {"name": "TotVAhImpPhB", "address": 40158, "length": 2, "type": "float32", "description": "Total VA-hours Imported phase B"},
    {"name": "TotVAhImpPhC", "address": 40160, "length": 2, "type": "float32", "description": "Total VA-hours Imported phase C"},
    {"name": "TotVArhImpQ1", "address": 40162, "length": 2, "type": "float32", "description": "Total VAR-hours Imported Q1"},
    {"name": "TotVArhImpQ1phA", "address": 40164, "length": 2, "type": "float32", "description": "Total VAR-hours Imported Q1 phase A"},
    {"name": "TotVArhImpQ1phB", "address": 40166, "length": 2, "type": "float32", "description": "Total VAR-hours Imported Q1 phase B"},
    {"name": "TotVArhImpQ1phC", "address": 40168, "length": 2, "type": "float32", "description": "Total VAR-hours Imported Q1 phase C"},
    {"name": "TotVArhImpQ2", "address": 40170, "length": 2, "type": "float32", "description": "Total VAR-hours Imported Q2"},
    {"name": "TotVArhImpQ2phA", "address": 40172, "length": 2, "type": "float32", "description": "Total VAR-hours Imported Q2 phase A"},
    {"name": "TotVArhImpQ2phB", "address": 40174, "length": 2, "type": "float32", "description": "Total VAR-hours Imported Q2 phase B"},
    {"name": "TotVArhImpQ2phC", "address": 40176, "length": 2, "type": "float32", "description": "Total VAR-hours Imported Q2 phase C"},
    {"name": "TotVArhExpQ3", "address": 40178, "length": 2, "type": "float32", "description": "Total VAR-hours Exported Q3"},
    {"name": "TotVArhExpQ3phA", "address": 40180, "length": 2, "type": "float32", "description": "Total VAR-hours Exported Q3 phase A"},
    {"name": "TotVArhExpQ3phB", "address": 40182, "length": 2, "type": "float32", "description": "Total VAR-hours Exported Q3 phase B"},
    {"name": "TotVArhExpQ3phC", "address": 40184, "length": 2, "type": "float32", "description": "Total VAR-hours Exported Q3 phase C"},
    {"name": "TotVArhExpQ4", "address": 40186, "length": 2, "type": "float32", "description": "Total VAR-hours Exported Q4"},
    {"name": "TotVArhExpQ4phA", "address": 40188, "length": 2, "type": "float32", "description": "Total VAR-hours Exported Q4 phase A"},
    {"name": "TotVArhExpQ4phB", "address": 40190, "length": 2, "type": "float32", "description": "Total VAR-hours Exported Q4 phase B"},
    {"name": "TotVArhExpQ4phC", "address": 40192, "length": 2, "type": "float32", "description": "Total VAR-hours Exported Q4 phase C"},
    {"name": "Evt", "address": 40194, "length": 2, "type": "bitfield32", "description": "Events"},
]

registers = [{**reg, "address": reg["address"] - 40000} for reg in complete_registers]

modbus_name_to_register_map = {
    item['name'] : item['address'] for item in registers
}


shelly_name_to_modbus_name_map = {
    # Phase A
    "a_current": "AphA",  # (40074)
    "a_voltage": "PhVphA",  # (40082)
    "a_act_power": "WphA",  # (40100)
    "a_aprt_power": "VAphA",  # (40108)
    "a_pf": "PFphA",  # (40124)
    "a_freq": "Hz",  # (40096)

    # Phase B
    "b_current": "AphB",  # (40076)
    "b_voltage": "PhVphB",  # (40084)
    "b_act_power": "WphB",  # (40102)
    "b_aprt_power": "VAphB",  # (40110)
    "b_pf": "PFphB",  # (40126)
    "b_freq": "Hz",  # (40096)

    # Phase C
    "c_current": "AphC",  # (40078)
    "c_voltage": "PhVphC",  # (40086)
    "c_act_power": "WphC",  # (40104)
    "c_aprt_power": "VAphC",  # (40112)
    "c_pf": "PFphC",  # (40128)
    "c_freq": "Hz",  # (40096)

    # Total Values
    "total_current": "A",  # (40072)
    "total_act_power": "W",  # (40098)
    "total_aprt_power": "VA",  # (40106)

    # Energy Data
    "a_total_act_ret_energy": "TotWhExpPhA",  # (40132)
    "a_total_act_energy": "TotWhImpPhA",  # (40140)
    "b_total_act_ret_energy": "TotWhExpPhB",  # (40134)
    "b_total_act_energy": "TotWhImpPhB",  # (40142)
    "c_total_act_ret_energy": "TotWhExpPhC",  # (40136)
    "c_total_act_energy": "TotWhImpPhC",  # (40144)
    "total_act_ret": "TotWhExp",  # (40130)
    "total_act": "TotWhImp",  # (40138)
}

def map_value_to_modbus_name(shelly_data):
    """Maps shelly data to modbus name, corrects signs and calculates additional values"""
    if shelly_data['a_act_power'] < 0:
        shelly_data['a_current'] = -shelly_data['a_current']
        if shelly_data['a_pf'] >0:
            shelly_data['a_pf'] = -shelly_data['a_pf']
    if shelly_data['b_act_power'] < 0:
        shelly_data['b_current'] = -shelly_data['b_current']
        if shelly_data['b_pf'] >0:
            shelly_data['b_pf'] = -shelly_data['b_pf']
    if shelly_data['c_act_power'] < 0:
        shelly_data['c_current'] = -shelly_data['c_current']
        if shelly_data['c_pf'] >0:
            shelly_data['c_pf'] = -shelly_data['c_pf']

    modbus_data = {shelly_name_to_modbus_name_map[key]: value for key, value in shelly_data.items() if key in shelly_name_to_modbus_name_map}

    A = shelly_data['a_current']+shelly_data['b_current']+shelly_data['c_current']
    modbus_data['A'] = A

    # Calculate phase-to-phase voltages
    PPVphAB = math.sqrt(3) * shelly_data["a_voltage"]
    PPVphBC = math.sqrt(3) * shelly_data["b_voltage"]
    PPVphCA = math.sqrt(3) * shelly_data["c_voltage"]
    PPV = (PPVphAB + PPVphBC + PPVphCA) / 3
    modbus_data["PPVphAB"] = PPVphAB
    modbus_data["PPVphBC"] = PPVphBC
    modbus_data["PPVphCA"] = PPVphCA
    modbus_data["PPVph"] = PPV

    # Calculate reactive power
    rad = shelly_data["a_aprt_power"] ** 2 - shelly_data["a_act_power"] ** 2
    VARphA = math.sqrt(rad) if rad > 0 else 0
    rad = shelly_data["b_aprt_power"] ** 2 - shelly_data["b_act_power"] ** 2
    VARphB = math.sqrt(rad) if rad > 0 else 0
    rad = shelly_data["c_aprt_power"] ** 2 - shelly_data["c_act_power"] ** 2
    VARphC = math.sqrt(rad) if rad > 0 else 0
    rad = shelly_data["total_aprt_power"] ** 2 - shelly_data["total_act_power"] ** 2
    VAR = math.sqrt(rad) if rad > 0 else 0

    modbus_data["VARphA"] = VARphA
    modbus_data["VARphB"] = VARphB
    modbus_data["VARphC"] = VARphC
    modbus_data["VAR"] = VAR

    # Calculate total power factor
    PF = (shelly_data["a_pf"] + shelly_data["b_pf"] + shelly_data["c_pf"]) / 3
    modbus_data["PF"] = PF

    return modbus_data

def map_values_to_registers(shelly_data):
    modbus_data = map_value_to_modbus_name(shelly_data)
    data = {modbus_name_to_register_map[key]: value for key, value in modbus_data.items() if key in modbus_name_to_register_map}
    return data
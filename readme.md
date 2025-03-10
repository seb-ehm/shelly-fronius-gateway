# Shelly Fronius Gateway  

This package provides a gateway that transforms **Shelly Pro 3EM** energy meter data into **Fronius-compatible Modbus** format.  

✅ **Tested with:** Fronius Gen24  
⚡ **Assumption:** The Shelly Pro 3EM is correctly installed, with channels **A, B, and C** corresponding to phases **L1, L2, and L3** as connected to the inverter.  

---

## 🚀 Usage  

### 🏃 Run Directly  

1. Install dependencies:  
   ```sh
   pip install -r requirements.txt

2. Create a config.json (see config.example.json)
3. Start the gatway:
   ```sh
   python main.py
4. Add the IP address of the computer running the gateway as a meter in your Fronius inverter settings.

---

### 🐳 Run with Docker
1. Create a config.json (see config.example.json)
2. Either put the config.json in the folder with the Dockerfile or mount it later
3. Build the docker image:
   ```sh
   docker build -t shelly-fronius-gateway .
4. Start the container, optionally with config.json mounted to the /app/ directory
   ```sh
   docker run -d --name shelly-fronius-gateway -v $(pwd)/config.json:/app/config.json shelly-fronius-gateway

5. Add the IP address of the machine running the container as a meter in your Fronius inverter settings.

### ⚙️ Configuration (`config.json`)  

Create a `config.json` file with the following options:  

| Option            | Type        | Description  |
|------------------|------------|-------------|
| `shelly_url`     | `string`    | The IP address or hostname of your **Shelly Pro 3EM** device.  |
| `shelly_offsets` | `object`    | Offsets subtracted from Shelly energy readings before conversion to Modbus. Helps prevent jumps in inverter statistics. |
| `nullify_channel` | `array`    | Disables specific measurement channels of the Shelly. Useful if a channel is **not measuring inverter production**. |

#### `shelly_offsets` Parameters  

| Key                      | Description |
|--------------------------|-------------|
| `a_total_act_energy`     | Offset for **phase A** total active energy (Wh). |
| `a_total_act_ret_energy` | Offset for **phase A** total active returned energy (Wh). |
| `b_total_act_energy`     | Offset for **phase B** total active energy (Wh). |
| `b_total_act_ret_energy` | Offset for **phase B** total active returned energy (Wh). |
| `c_total_act_energy`     | Offset for **phase C** total active energy (Wh). |
| `c_total_act_ret_energy` | Offset for **phase C** total active returned energy (Wh). |
| `total_act`              | Offset for total active energy (Wh). |
| `total_act_ret`          | Offset for total active returned energy (Wh). |

**Example `config.json`:**  
```json
{
    "shelly_url": "http://shellypro3em/rpc/Shelly.GetStatus",
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
    "nullify_channel": ['c']
}
```

---

### 🔗 Additional Notes

Offsets are recommended to prevent inconsistencies in Fronius SolarWeb statistics.
Nullify channels if a Shelly Pro 3EM channel is measuring something unrelated to inverter production.
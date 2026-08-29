# ☀️ SynCoin Universal Solar & Battery (BESS) Guide

> **Version** : v1.0.0 — MIT License  
> **Concept** : Residential Micro-Neocloud (Downscaling 1/100e of Industrial Datacenters)  
> **Supported Hardware** : Tesla Powerwall, Enphase Envoy, SolarEdge, EcoFlow, Victron Energy, Huawei LUNA, BYD, Shelly Pro EM

---

## ⚡ The Economic & Physical Thesis

Industrial datacenters face a **3 to 6-year waiting line** to connect to saturated electrical grids. Meanwhile, millions of homes generate **surplus solar power** that is either curtailed or sold back at 0.05–0.08 €/kWh.

**SynCoin converts this fatal surplus directly into AI Inférence**:
- Value when sold to grid : ~0.08 €/kWh
- Value when converted to AI Inférence via SynCoin : **0.50 € to 1.20 € equivalent per kWh**
- **Payback Time** : Reduces home battery & solar ROI from 12 years down to **1.9 years**.

---

## 🏗️ Hardware Architecture & Flow

```
┌─────────────────┐       ┌────────────────────────┐       ┌─────────────────┐
│ ☀️ Solar Panels │ ────► │ ⚡ Inverter / Battery  │ ────► │ 🏠 Home Needs   │
│ (1 kW to 10 kW) │       │ (Tesla, Enphase, BYD)  │       │ (Base: ~300 W)  │
└─────────────────┘       └───────────┬────────────┘       └─────────────────┘
                                      │
                         Surplus (P_solar - P_home)
                                      ▼
                          ┌────────────────────────┐
                          │ 🧠 SynCoin Energy      │
                          │    Arbiter Daemon      │
                          └───────────┬────────────┘
                                      │
                 ┌────────────────────┴────────────────────┐
                 ▼                                         ▼
    ┌─────────────────────────┐               ┌─────────────────────────┐
    │ 🖥️ Desktop GPU / Mac    │               │ 📱 Charging Phones      │
    │ (Mistral / SLMs / CUDA) │               │ (WASM / Apple Silicon)  │
    └─────────────────────────┘               └─────────────────────────┘
```

---

## ⚙️ Mathematical Arbitrage Logic

The daemon [`syncoin_energy_daemon.py`](../syncoin_energy_daemon.py) evaluates 4 distinct states every 5 seconds:

### 1. `GREEN_SOLAR` (Direct Solar Inférence)
$$\text{Condition: } P_{\text{solar}} - P_{\text{home}} \ge 250\text{ W}$$
- 100% of GPU/CPU computing power is unleashed on the clean surplus.
- Zero draw from the public electrical grid.

### 2. `GREEN_BATTERY` (Peak Hours Arbitrage)
$$\text{Condition: } \text{Battery SoC} \ge 80\% \quad \text{and} \quad \text{Battery SoC} > \text{Reserve}$$
- Computes from stored green energy during global AI peak demand hours.

### 3. `BATTERY_RESERVE_HOLD` (Emergency Home Protection)
$$\text{Condition: } \text{Battery SoC} \le 30\%$$
- Compute is halted immediately to reserve electricity for essential household appliances.

### 4. `PAUSED`
$$\text{Condition: } \text{Night without battery surplus}$$
- Nodes remain in ultra-low power standby (0.5 W).

---

## 🔌 Integration with Home Automation (Home Assistant / MQTT)

### 1. Home Assistant Add-on / MQTT
Publish solar and battery power to MQTT:
```json
// Topic: homeassistant/sensor/solar_power/state
{ "watts": 1850 }

// Topic: homeassistant/sensor/battery_soc/state
{ "soc": 85.4 }
```

### 2. Run the SynCoin Energy Daemon
```bash
# Connect to your local MQTT/NATS broker
python3 syncoin_energy_daemon.py --nats nats://localhost:4222
```

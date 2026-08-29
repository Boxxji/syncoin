# 🏛️ SynCoin Global Mesh Architecture v1.0

> **Version** : v1.0.0 — MIT License  
> **Topology** : P2P Distributed Mesh + NATS Event Broker + OpenAI Gateway

---

## 🌐 Full System Topology

```
                  ┌─────────────────────────────────────────┐
                  │  🏢 Client Companies & AI Developers   │
                  └────────────────────┬────────────────────┘
                                       │ HTTP REST (/v1/chat/completions)
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │   🌐 SynCoin Gateway & Marketplace      │
                  │        (syncoin_gateway.py :8767)       │
                  └────────────────────┬────────────────────┘
                                       │ NATS (syncoin.jobs)
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │   🧠 SynCoin P2P Node Hub (Sun-Follower)│
                  │         (syncoin_node.py :8766)         │
                  └────────┬───────────┬───────────┬────────┘
                           │           │           │
       ┌───────────────────┘           │           └───────────────────┐
       ▼                               ▼                               ▼
┌──────────────┐               ┌──────────────┐               ┌──────────────┐
│  🖥️ Desktop  │               │ 📱 iOS App   │               │ 🤖 Android   │
│ (macOS/Win)  │               │ (SwiftUI)    │               │ (Flutter)    │
│ CUDA/Metal   │               │ Wasm3 Engine │               │ NPU/WASM     │
└──────┬───────┘               └──────┬───────┘               └──────┬───────┘
       │                               │                               │
       ▼                               ▼                               ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                  ⚡ Residential Micro-Neocloud (Energy Layer)              │
│       ☀️ Solar Panels (1-10 kW)  +  🔋 Home Batteries (Tesla, BYD)         │
│               syncoin_energy_daemon.py (MQTT / Modbus)                     │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔑 Core Architecture Pillars

1. **Energy-First Inférence Routing (Sun-Follower)**:
   - When requests arrive at the Gateway, the SynCoin Hub dispatches them preferentially to workers with active solar surplus (`GREEN_SOLAR`) or high battery charge (`GREEN_BATTERY`).
2. **WebAssembly Sandbox (Wasm3)**:
   - Untrusted compute tasks are strictly isolated in embedded Wasm3 sandboxes on iPhones, Androids, and desktops.
3. **Smart Settlement (90/10 Proof of Compute)**:
   - Proof of inference hashes (SHA-256) trigger instant Olona token and Solana micro-rewards.

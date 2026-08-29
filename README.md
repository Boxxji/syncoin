# SynCoin 🌱 — Universal Decarbonized AI Compute Network

**Transform your solar surplus, residential batteries, and idle smartphones into a green, decentralized AI supercomputer.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](syncoin_node.py)
[![iOS](https://img.shields.io/badge/iOS-SwiftUI%20%2B%20Wasm3-orange.svg)](ios/)
[![NATS](https://img.shields.io/badge/Broker-NATS%20High--Velocity-blue.svg)](https://nats.io)
[![Solana](https://img.shields.io/badge/Solana-Smart%20Contracts-purple.svg)](contracts/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

SynCoin is a **100% Free & Open-Source (MIT)** decentralized compute network. It operates as a **Residential Micro-Neocloud** that unifies home solar panels, battery energy storage systems (BESS), desktop GPUs, and smartphones into a global, sovereign, and carbon-negative compute mesh.

---

## ⚡ The Core Problem & The SynCoin Solution

- **Cloud Saturation & Energy Bottleneck**: Centralized AI datacenters face 3 to 6-year grid connection delays and massive water consumption.
- **Wasted Solar & Battery Surplus**: Millions of homes generate fatal solar energy that is sold back to the grid at low rates.
- **The SynCoin Model (Energy-First Compute)**: Move the compute to where clean energy already exists (**Grid Bypass**). Monétisez votre surplus solaire ou batterie sous forme d'inférence IA utile pour la recherche, les universités et les modèles ouverts (Mistral, Llama, DeepSeek).

---

## 🏗️ Universal 4-Layer Architecture

```mermaid
graph TD
    subgraph "1. Clean Energy Capture"
        Solar["☀️ Solar Panels (1-10 kW)"] --> Inverter["⚡ Smart Meter / Inverter (MQTT / Modbus)"]
        Battery["🔋 Home Battery (Tesla, Enphase, EcoFlow, BYD)"] <--> Inverter
    end

    subgraph "2. SynCoin Energy Arbiter"
        Inverter --> Arbiter["🧠 Energy Daemon (Surplus Arbitrage)"]
        Arbiter --> Node["🌐 SynCoin P2P Node (NATS :4222 / WS :8766)"]
    end

    subgraph "3. Distributed Workers"
        Node --> Phone["📱 Smartphones (iOS Wasm3 / Android NPU)"]
        Node --> PC["🖥️ Desktops & Servers (Nvidia CUDA / Apple Metal / AMD)"]
    end

    subgraph "4. Decarbonized Value"
        Phone --> Proof["🪙 Proof of Green Compute"]
        PC --> Proof
        Proof --> Rewards["🌱 Olona Tokens / ASBL Planted Trees / Solana"]
    end
```

---

## 🚀 Key Capabilities

1. **🔋 Residential Micro-Neocloud & Battery Arbitrage**:
   - Automatic detection of solar surplus ($P_{\text{solar}} - P_{\text{home}} > \text{threshold}$) via Home Assistant, MQTT, or Modbus.
   - Dynamic power modulation: AI inference kicks in when energy is green and free, and pauses when home needs electricity.
   - Battery Health Guard: Preserves battery cycle life and guarantees emergency power reserve ($>30\%$).

2. **📱 Smartphone Edge Compute (iOS & Android)**:
   - Zero-friction background computing via embedded **Wasm3 WebAssembly runtime** and Apple Silicon Neural Engine.
   - **Guaranteed Eco-Safeguards**: Executes **only** when plugged into AC power, fully charged, on WiFi, and thermally nominal.

3. **🔬 Useful Public-Good AI**:
   - SLM Inférence (Small Language Models: Qwen, SmolLM, Phi, Gemma).
   - Cetacean Bioacoustics & Marine Research (Zero-Supervision t-SNE / CETI project).
   - Climate modeling, medical R&D, and open science.

4. **🌱 Ecological Economics**:
   - **Olona Tokens**: Transparent compute contribution tracking.
   - **Tree Planting ASBL**: Automatic burning of Olona tokens to plant verified trees worldwide.

---

## 📦 Quick Start & Applications Multi-Plateformes

### 1. 🖥️ Application Desktop (macOS & Windows PC)
Lancez l'interface graphique de bureau avec jauges solaires et gains en direct :
```bash
cd desktop
python3 desktop_app.py
```
*Pour générer l'exécutable autonome (`.app` ou `.exe`) :*
```bash
python3 package_desktop.py
```

### 2. 📱 Application iOS Native (iPhone & iPad)
- Ouvrez `ios/SynCoin.xcodeproj` dans **Xcode**.
- Connectez votre iPhone ou lancez le simulateur.
- L'application active automatiquement le moteur **Wasm3** sur processeur Apple Silicon lorsque l'appareil est branché sur secteur/solaire.

### 3. 🤖 Application Android & Mobile (Flutter)
```bash
cd mobile/app
flutter pub get
flutter run
```

### 4. 🌐 Gateway d'Inférence & Marketplace (Compatible OpenAI)
Démarrez la passerelle permettant aux entreprises et développeurs de consommer de l'inférence décarbonée :
```bash
python3 syncoin_gateway.py
```
**Exemple d'appel client (curl) :**
```bash
curl -X POST http://localhost:8767/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "syncoin-green-slm",
    "messages": [{"role": "user", "content": "Quelle est l'\''importance du calcul décarboné ?"}]
  }'
```
*Réponse instantanée avec règlement financier automatique (90% au producteur particulier / 10% ASBL Arbres).*

---

## 💰 Modèle Économique & Rémunération Équitable

| Rôle | Flux Financier / Énergétique | Rémunération |
| :--- | :--- | :--- |
| **Producteur Particulier** (Mac, PC, iPhone, Android) | Fournit le surplus solaire / batterie et la puissance GPU/NPU. | **90% des revenus d'inférence** versés instantanément en Tokens Olona / Solana. |
| **Planète & Écologie (ASBL)** | Reforestation mondiale certifiée. | **10% des revenus** convertis automatiquement pour planter des arbres. |
| **Client / Entreprise** | Envoie ses requêtes via l'API OpenAI standard. | Inférence IA décarbonée, souveraine et jusqu'à 70% moins chère que les hyperscalers. |

---

## 📜 License & Open Source

This project is licensed under the **MIT License** — free and open for the entire world.

🌱 *For Lilo, for the world, for all of us. Built with love and sovereign green energy.*

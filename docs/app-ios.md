# 📱 SynCoin Native iOS Application Guide (iPhone & iPad)

> **Version** : v1.0.0 — MIT License  
> **Framework** : SwiftUI + Wasm3 Embedded C Engine + Accelerate vDSP  
> **Compatibility** : iOS 16.0+, iPadOS 16.0+, Apple Silicon (A14 à A18 Pro / M-Series)

---

## 🌟 Overview

The **SynCoin iOS App** turns your idle iPhone or iPad into an edge compute node while you sleep or charge. Powered by an embedded **Wasm3 WebAssembly interpreter** and Apple's **Accelerate / Metal framework**, it securely executes micro-tasks of AI inférence and bioacoustic analysis directly on device.

```
┌──────────────────────────────────────────────────────────┐
│  🌱 SYNCOIN OS v1.0                     [● EN CHARGE]    │
├──────────────────────────────────────────────────────────┤
│  SOLDE RÉMUNÉRATION                                      │
│  100.05 🌱 (+0.05 Olona par lot)                         │
│  Adresse Solana : 7xK2...9pQr (Devnet/Mainnet)           │
├──────────────────────────────────────────────────────────┤
│  🛡️ GARDE-FOUS ÉCOLOGIQUES                              │
│  🔌 Alimentation : Branché sur Secteur / Charge Solaire  │
│  🔋 Batterie : 100% (Seuil minimal : > 80%)              │
│  🌡️ État Thermique : Nominal (Arrêt auto si chaud)       │
├──────────────────────────────────────────────────────────┤
│  📜 JOURNAL EN DIRECT                                    │
│  > WASM MODULE LOADED: test_hash                         │
│  > EXECUTION TIME: 0.19ms | GFLOPS: 32.4                 │
│  > PROOF OF COMPUTE SENT TO HUB                          │
└──────────────────────────────────────────────────────────┘
```

---

## 🛡️ Eco-Computing Rules (Zero-Wear Guarantee)

To guarantee that your iPhone's battery and user experience are never degraded:
1. **AC / Solar Charging Condition**: The compute engine executes **only** when `UIDevice.batteryState == .charging` or `.full`.
2. **Thermal Safeguard**: Execution pauses instantly if `ProcessInfo.thermalState` rises above `.nominal`.
3. **WiFi Only**: Zero data consumed on 4G/5G mobile plans.

---

## 🏗️ Technical Architecture

- **`SynCoinApp.swift`**: SwiftUI interface with real-time WebSocket connection to the SynCoin Hub (`ws://...:8766`).
- **`WasmEngine.swift`**: Swift wrapper around the high-speed C interpreter `wasm3`.
- **`ios/wasm3/`**: Embedded C WebAssembly runtime compiling directly within Xcode without external dependencies.
- **`Accelerate.framework`**: vDSP BLAS matrix multiplication (`cblas_sgemm`) for benchmark and neural weight acceleration.

---

## 📦 Build & Installation via Xcode

1. Open `ios/SynCoin.xcodeproj` in **Xcode 15+**.
2. Select your development team in *Signing & Capabilities*.
3. Connect your physical iPhone or iPad via USB/WiFi.
4. Hit **Run (⌘ + R)**.
5. In *Settings > General > VPN & Device Management*, trust your developer certificate.
6. Plug your phone into power — the app connects to the nearest Hub and automatically starts earning Olona tokens!

---

## 🪙 Rewards & Tree Staking

- Earn **0.05 Olona** per verified micro-job.
- Tap **"Plant a Tree"** in the app to burn 50 Olona: a real tree is planted and verified via our non-profit ASBL partner.

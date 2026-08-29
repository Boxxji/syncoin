# Changelog — SynCoin 🌱

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-08-29 — *Universal Decarbonized AI Mesh (MIT Release)*

### 🚀 Added
- **MIT License Release**: 100% free and open-source for the world (developers, universities, researchers, households).
- **Residential Micro-Neocloud (Solar & Battery BESS)**:
  - `syncoin_energy_daemon.py`: Real-time tracking of photovoltaic surplus ($P_{\text{solar}} - P_{\text{home}}$) and battery state of charge ($SoC\%$) via MQTT/Modbus/Home Assistant.
- **OpenAI-Compatible Inférence Gateway & Remuneration Marketplace**:
  - `syncoin_gateway.py` (`POST /v1/chat/completions`, `GET /v1/models`, `GET /v1/marketplace/stats`): Enables companies and developers to consume clean inference with **100% direct remuneration** paid to compute hosts.
- **Multi-Platform Client Applications**:
  - **macOS & Windows PC**: `desktop/desktop_app.py` (Graphical Desktop App with live solar gauges, TOPS counter and direct payout ledger) + `desktop/package_desktop.py`.
  - **iOS Native (iPhone/iPad)**: `ios/SynCoinApp.swift` with embedded C `WasmEngine.swift` (Wasm3 runtime) and strict thermal/charging safeguards.
  - **Android (Flutter/Dart)**: `mobile/app/lib/main.dart` with WebSocket client, live green terminal, and wallet manager.
- **Automated End-to-End Test Suite**:
  - `tests/test_syncoin_e2e.py`: 16 automated tests covering the full cycle with 100% pass rate.
- **Comprehensive English Documentation Suite**:
  - `docs/app-macos-windows.md`, `docs/app-ios.md`, `docs/app-android.md`, `docs/solar-batteries-guide.md`, `docs/gateway-openai-api.md`.

---

## [0.2.0] - 2026-07-19
- Native iOS SwiftUI application with vDSP Accelerate execution.
- High-velocity NATS broker integration.
- Standalone P2P node deployment on port `:8766`.

---

## [0.1.0] - 2026-06-30
- Initial P2P Node implementation (`syncoin_node.py`).
- Bioacoustic CETI t-SNE worker protocol.
- Smart Contracts Solana (Olona token & direct reward settlement).

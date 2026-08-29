# Changelog — SynCoin 🌱

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-08-29 — *Universal Decarbonized AI Mesh (MIT Release)*

### 🚀 Added
- **Licence MIT Standard (2026)** : Ouverture totale et gratuite pour le monde entier (développeurs, universités, chercheurs, particuliers).
- **Residential Micro-Neocloud (Solar & Battery BESS)** :
  - `syncoin_energy_daemon.py` : Détection du surplus photovoltaïque ($P_{\text{solar}} - P_{\text{home}}$) et du niveau de charge batterie ($SoC\%$) via MQTT/Modbus/Home Assistant.
- **OpenAI-Compatible Inférence Gateway & Remuneration Marketplace** :
  - `syncoin_gateway.py` (`POST /v1/chat/completions`, `GET /v1/models`, `GET /v1/marketplace/stats`) : Permet aux entreprises de consommer de l'inférence décarbonée et rémunère automatiquement les producteurs particuliers à hauteur de 90% (10% pour l'ASBL Reforestation).
- **Multi-Platform Client Applications** :
  - **macOS & Windows PC** : `desktop/desktop_app.py` (Application graphique complète avec monitoring en temps réel des gains et de l'énergie solaire) + `desktop/package_desktop.py`.
  - **iOS Native (iPhone/iPad)** : `ios/SynCoinApp.swift` avec moteur d'exécution WebAssembly `WasmEngine.swift` (Wasm3 C runtime).
  - **Android (Flutter/Dart)** : `mobile/app/lib/main.dart` avec client WebSocket, terminal en direct et gestionnaire de portefeuille.
- **Automated End-to-End Test Suite** :
  - `tests/test_syncoin_e2e.py` : 16 tests validés avec 100% de succès.

---

## [0.2.0] - 2026-07-19
- Intégration de l'application native iOS SwiftUI avec exécution vDSP Accelerate.
- Support du Broker NATS pour l'injection de jobs haute vélocité.
- Déploiement du conteneur VPS sur port `:8766`.

---

## [0.1.0] - 2026-06-30
- Initial P2P Node implementation (`syncoin_node.py`).
- Bioacoustic CETI t-SNE worker protocol.
- Smart Contracts Solana (Olona token & ASBL Tree Planting).

### For Lilo
This project is dedicated to the memory of a good and kind friend.
Every planted tree, every Olona offered, every compute shared is for you.
🌱💜

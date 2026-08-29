# 🤖 SynCoin Android Mobile Application Guide

> **Version** : v1.0.0 — MIT License  
> **Framework** : Flutter / Dart (Material 3)  
> **Compatibility** : Android 9.0+ (API 28+), Snapdragon NPU, Google Tensor, MediaTek

---

## 🌟 Overview

The **SynCoin Android App** is a sovereign mobile compute worker built with Flutter. It allows Android smartphones and tablets to participate in the global green compute mesh, executing AI micro-tasks while charging.

```
┌──────────────────────────────────────────────────────────┐
│  NET: ONLINE       OLONA: 100.25       CYCLES: 450       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  > SYNCOIN OS v1.0 INITIALIZED                           │
│  > P2P PROTOCOL: CONNECTED TO ws://127.0.0.1:8766        │
│  > GREEN POWER PROBE: AC MAINS CONNECTED                 │
│  > COMPUTE_BATCH [CYCLES: 15] EXECUTED                   │
│  > PROOF HASH: e4a1...9b2c RECORDED                      │
│  > REWARD CREDITED: +0.05 OLONA 🌱                       │
│                                                          │
├──────────────────────────────────────────────────────────┤
│  [🛑 STOP GREEN COMPUTE]                                 │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Features

1. **Reactive Material 3 UI**: Dark terminal aesthetics with real-time green neon logs.
2. **WebSocket P2P Client**: Auto-reconnects to local or cloud hubs with sub-millisecond dispatching.
3. **Integrated Olona & Tree Wallet**: Tracks compute rewards, Solana public keys, and reforestation counters.
4. **Android WorkManager / Background Service**: Operates seamlessly as an Android foreground service when plugged in.

---

## 📦 Build & Run Instructions

### Prerequisites
- Flutter SDK 3.19+
- Android Studio / Android SDK Tools
- Java 17+

### 1. Run in Development Mode
```bash
cd mobile/app
flutter pub get
flutter run
```

### 2. Build Release APK for Distribution (F-Droid / Play Store)
```bash
cd mobile/app
flutter build apk --release
```
The compiled, standalone APK will be generated at:
`mobile/app/build/app/outputs/flutter-apk/app-release.apk`

---

## 🔒 Permissions & Privacy

- `android.permission.INTERNET` : P2P WebSocket communication with the Hub.
- `android.permission.ACCESS_NETWORK_STATE` : WiFi vs Mobile data detection.
- `android.permission.BATTERY_STATS` : Power plug detection.
- **Zero Tracking**: No Google Analytics, no Firebase, no ads. 100% open-source under MIT License.

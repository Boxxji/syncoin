# 🛠️ SynCoin Universal Installation & Deployment Guide

> **Version** : v1.0.0 — MIT License

---

## ⚡ 1-Minute Quick Start

### 1. Hub Node & Energy Gateway (Server / Cloud / VPS)
```bash
# Clone the repository
git clone https://github.com/Boxxji/syncoin.git
cd syncoin

# Install dependencies
pip install -r requirements.txt

# Start P2P Hub (Port 8766) and OpenAI Gateway (Port 8767)
python3 syncoin_node.py --port 8766 &
python3 syncoin_gateway.py &
```

---

## 🖥️ 2. Desktop Client (macOS & Windows)
```bash
cd desktop
python3 desktop_app.py
```
*See [Desktop App Guide](app-macos-windows.md) for compiling `.app` / `.exe` binaries.*

---

## 📱 3. Native iOS App (iPhone / iPad)
- Open `ios/SynCoin.xcodeproj` in **Xcode**.
- Connect your device and press **Run**.
- *See [iOS App Guide](app-ios.md).*

---

## 🤖 4. Android Mobile App (Flutter)
```bash
cd mobile/app
flutter pub get
flutter run
```
*See [Android App Guide](app-android.md).*

---

## ☀️ 5. Solar & Battery Arbiter Daemon
```bash
# Connect to your home solar inverter / Home Assistant MQTT
python3 syncoin_energy_daemon.py --nats nats://localhost:4222
```
*See [Solar & Batteries Guide](solar-batteries-guide.md).*

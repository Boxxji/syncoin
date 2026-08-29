# 🖥️ SynCoin Desktop Application Guide (macOS & Windows PC)

> **Version** : v1.0.0 — MIT License  
> **Target Systems** : macOS (Apple Silicon M1/M2/M3/M4 & Intel), Windows 10/11 (Nvidia, AMD, Intel)

---

## 🌟 Overview

The **SynCoin Desktop App** is a lightweight, high-performance sovereign graphical client that enables anyone with a Mac or Windows PC to monetize their idle GPU/CPU power using green energy (solar surplus or home batteries).

```
┌───────────────────────────────────────────────────────────────┐
│  🌱 SynCoin Desktop Mesh v1.0         [● INFÉRENCE ACTIVE]   │
├───────────────────────────────────────────────────────────────┤
│  SOLDE RÉMUNÉRATION       TÂCHES IA COMPLÉTÉES   IMPACT ÉCO   │
│  100.00 🌱 (≈ 50.00 €)    142 micro-jobs         4 🌲 plantés │
├───────────────────────────────────────────────────────────────┤
│  ⚡ ARBITRAGE ÉNERGÉTIQUE (MICRO-NEOCLOUD)                    │
│  ☀️ Solaire : 1250 W [████████████░░░░]                       │
│  🔋 Batterie BESS : 88% [████████████████░]                  │
├───────────────────────────────────────────────────────────────┤
│  [🛑 PAUSE DU CALCUL DÉCARBONÉ]                               │
├───────────────────────────────────────────────────────────────┤
│  📜 JOURNAL D'INFÉRENCE & PREUVES EN DIRECT                   │
│  [19:33:46] Inférence SLM complétée en 50.62ms. Preuve SHA OK │
└───────────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Features

1. **Live Remuneration Dashboard**: Real-time display of Olona token balance, euro equivalent, and trees planted.
2. **Solar & Battery Integration**: Synchronizes with your home energy daemon to only consume surplus clean energy.
3. **Multi-Accelerator Engine**: Automatically leverages **Apple Metal / Neural Engine** on macOS, **Nvidia CUDA** or **AMD ROCm** on Windows/Linux, or multithreaded CPU fallback.
4. **1-Click Operation**: No terminal knowledge required. Hit "Start Green Mining" and let your computer generate revenue.

---

## 📦 Installation & Execution

### Option A : Direct Python Launch (Zero Install)
```bash
# Clone the repository
git clone https://github.com/Boxxji/syncoin.git
cd syncoin/desktop

# Install lightweight UI dependencies
pip install -r ../requirements.txt

# Run the Desktop Application
python3 desktop_app.py
```

### Option B : Standalone Binary Packaging (.app / .exe)
You can compile a standalone executable that runs without Python:
```bash
cd desktop
python3 package_desktop.py
```
- **macOS** : Generates `desktop/dist/SynCoin-Desktop-Mac.app`
- **Windows** : Generates `desktop/dist/SynCoin-Desktop-Windows.exe`

---

## ⚙️ Energy Modes Configuration

| Mode | Trigger Condition | Hardware Behavior |
| :--- | :--- | :--- |
| **Solar Priority (Default)** | $P_{\text{solar}} - P_{\text{home}} \ge 250\text{W}$ | Computes 100% on green surplus. Automatically pauses if clouds pass. |
| **Battery Arbitrage** | Battery SoC $\ge 80\%$ | Computes from home battery storage during peak global inference demand. |
| **Continuous / Grid** | User forced ON | Operates 24/7 on standard AC mains power. |

---

## 🔒 Security & Privacy (MIT Guarantees)

- **Zero Data Leakage**: Inférence prompts processed by your GPU/WASM engine are memory-isolated and discarded immediately after proof computation.
- **No Telemetry / No Tracking**: 100% open source under the MIT License.

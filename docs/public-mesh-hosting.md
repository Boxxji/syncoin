# 🌐 SynCoin Free & Open Public Mesh Hosting Guide

> **Version** : v1.0.0 — MIT License  
> **Core Principle** : 100% Free, Zero-Server-Cost & Independent Public Infrastructure

---

## 🌟 The Philosophy: Zero Private Infrastructure Dependency

SynCoin is designed from the ground up to **never depend on any private server, proprietary cloud account, or centralized coordinator**. Any citizen, student, developer, or university can participate in or host a public SynCoin Hub using **free, open-source community infrastructure**.

```
                           ┌────────────────────────────────────────┐
                           │   FREE PUBLIC COMMUNITY INFRASTRUCTURE │
                           └───────────────────┬────────────────────┘
                                               │
             ┌─────────────────────────────────┼─────────────────────────────────┐
             ▼                                 ▼                                 ▼
┌─────────────────────────┐       ┌─────────────────────────┐       ┌─────────────────────────┐
│ 🤗 Hugging Face Spaces  │       │ ⚡ Open Nostr Relays    │       │ 🌐 WebRTC / Free STUN   │
│ (Free 24/7 Cloud Hub)   │       │ (Decentralized Pub/Sub) │       │ (Direct P2P Browser/OS) │
│ hf.space/ws             │       │ wss://relay.damus.io    │       │ stun:stun.l.google.com  │
└─────────────────────────┘       └─────────────────────────┘       └─────────────────────────┘
```

---

## 1. 🤗 Option A: Free 1-Click Hugging Face Space Hub

Hugging Face provides free 24/7 CPU/Docker instances with free subdomains, HTTPS, and persistent WebSocket support.

### How to Deploy Your Own Free Hub:
1. Create a free account on [Hugging Face](https://huggingface.co).
2. Go to **Spaces > Create New Space**.
3. Set **SDK: Docker** (Port `7860`).
4. Push or copy the files in the [`huggingface/`](../huggingface/) directory (`app.py`, `Dockerfile`, `requirements.txt`, `README.md`).
5. **Done!** Your public Hub is live at `https://<your-username>-syncoin-hub.hf.space` with:
   - WebSocket worker entrypoint: `wss://<your-username>-syncoin-hub.hf.space/ws`
   - OpenAI-compatible REST API: `https://<your-username>-syncoin-hub.hf.space/v1/chat/completions`

---

## 2. ⚡ Option B: Open Nostr Decentralized Relays

For censorship-resistant, zero-server job coordination:
- Nodes announce their compute capacity over public Nostr relays:
  - `wss://relay.damus.io`
  - `wss://relay.nostr.band`
  - `wss://nos.lol`
- Compute requests are broadcasted as signed Nostr events. Nearest solar workers pick up the event, execute inference, and publish the proof hash back to the relay.

---

## 3. 🌐 Option C: Direct WebRTC & Free Public STUN Servers

For direct browser-to-browser and device-to-device streaming:
- Devices perform NAT traversal using free public STUN servers:
  - `stun:stun.l.google.com:19302`
  - `stun:stun.cloudflare.com:3478`
- Once connected, data flows directly peer-to-peer over encrypted WebRTC DataChannels with **0 bytes passing through any server**.

---

## 📡 Option D: Public NATS Demo Broker

For testing and rapid multi-agent prototyping, SynCoin supports the open NATS community demo cluster:
```bash
python3 syncoin_node.py --nats nats://demo.nats.io:4222
```

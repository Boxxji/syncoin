# SynCoin Technical Architecture

```
┌─────────┐    ┌──────────┐    ┌──────────┐
│  Phone  │◄──►│   P2P    │◄──►│  Solana  │
│ (Flutter)│    │ (Python) │    │ (Ledger) │
└─────────┘    └──────────┘    └──────────┘
```
## P2P Protocol (Upgraded for Bioacoustics)
- Port: 8766 (default)
- Transport: WebSocket (WSS) / JSON
- Actions: ping, compute, stats, peers
- **Proof of Compute**: Zéro-Supervision Latent Space (t-SNE) on Bioacoustic Codas (128D Embeddings).
- **Security**: S1-FAIL-FAST enforcement on mathematical corruption (NaN).

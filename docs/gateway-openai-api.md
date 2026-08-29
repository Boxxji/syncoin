# 🌐 SynCoin OpenAI-Compatible Inférence Gateway & Remuneration Marketplace

> **Version** : v1.0.0 — MIT License  
> **Base URL** : `http://localhost:8767` (or `http://168.231.83.190:8767` in Production)  
> **API Standard** : 100% Compatible OpenAI v1 Specification (`/v1/chat/completions`, `/v1/models`)

---

## 🌟 Overview

The **SynCoin Inférence Gateway** acts as a decentralized compute marketplace. It allows companies, researchers, and developers to submit standard OpenAI API prompts while automatically routing them to green edge workers (Macs, PCs, iPhones, Android devices running on solar surplus or batteries).

### Key Highlights:
- **70% Cheaper** than traditional hyperscaler clouds (AWS, GCP, Azure).
- **Carbon-Negative & Sovereign**: Every request includes verified proof of green compute.
- **Smart Remuneration (90/10 Split)**: 90% of token value goes directly to the solar/battery host, 10% funds real-world reforestation via our non-profit ASBL partner.

---

## 📡 API Endpoints Reference

### 1. List Available Models
`GET /v1/models`

**Response:**
```json
{
  "object": "list",
  "data": [
    {
      "id": "syncoin-green-slm",
      "object": "model",
      "created": 1788020000,
      "owned_by": "syncoin-mesh",
      "description": "Green Decarbonized SLM (Powered by Solar & Battery Mesh)"
    },
    {
      "id": "syncoin-wasm-inference",
      "object": "model",
      "created": 1788020000,
      "owned_by": "syncoin-mesh",
      "description": "WebAssembly Neural Micro-Tasks (iPhones, Android, Desktops)"
    }
  ]
}
```

---

### 2. Create Chat Completion
`POST /v1/chat/completions`

**Headers:**
- `Content-Type: application/json`

**Request Body:**
```json
{
  "model": "syncoin-green-slm",
  "messages": [
    {
      "role": "user",
      "content": "Explain the concept of decentralized green AI in one sentence."
    }
  ]
}
```

**Response (OpenAI Standard + SynCoin Settlement Meta):**
```json
{
  "id": "req-1788024826682-f9d2f8",
  "object": "chat.completion",
  "created": 1788024826,
  "model": "syncoin-green-slm",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "[SynCoin Green Inférence (Solaire 100%)]: Decentralized green AI moves compute to renewable energy sources directly at the residential level."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 46,
    "total_tokens": 58
  },
  "syncoin_settlement": {
    "producer_worker_id": "worker-green-edge",
    "energy_source": "GREEN_SOLAR",
    "worker_payout_olona": 0.207,
    "asbl_trees_funded": 0.023,
    "inference_duration_ms": 50.62
  }
}
```

---

### 3. Get Marketplace & Remuneration Statistics
`GET /v1/marketplace/stats`

**Response:**
```json
{
  "status": "online",
  "mesh": "SynCoin Decarbonized Compute Mesh",
  "total_tokens_inferred": 145000,
  "total_olona_distributed": 725.50,
  "total_trees_funded": 14.51,
  "producers_count": 8,
  "producers": [
    {
      "worker_id": "worker-mac-solar-01",
      "total_olona": 120.45,
      "total_jobs": 240,
      "energy_source": "GREEN_SOLAR",
      "solana_wallet": "sol_mac_payout"
    }
  ]
}
```

---

## 💻 Code Integration Examples

### Python (using Official OpenAI SDK)
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8767/v1",
    api_key="syncoin-community-free" # Zero-friction access
)

response = client.chat.completions.create(
    model="syncoin-green-slm",
    messages=[
        {"role": "user", "content": "How does SynCoin reward solar producers?"}
    ]
)

print(response.choices[0].message.content)
```

---

### JavaScript / TypeScript (Node.js & Browser)
```javascript
import OpenAI from "openai";

const openai = new OpenAI({
  baseURL: "http://localhost:8767/v1",
  apiKey: "syncoin-community-free",
});

async function main() {
  const completion = await openai.chat.completions.create({
    model: "syncoin-green-slm",
    messages: [{ role: "user", content: "Tell me a short green quote." }],
  });

  console.log(completion.choices[0].message.content);
}

main();
```

---

### cURL
```bash
curl -X POST http://localhost:8767/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "syncoin-green-slm",
    "messages": [{"role": "user", "content": "Hello SynCoin Green Mesh!"}]
  }'
```

import asyncio
import nats
import json

import os
import nats

async def send_job():
    nats_url = os.environ.get("NATS_URL", "nats://localhost:4222")
    try:
        nc = await nats.connect(nats_url)
        payload = json.dumps({
            "action": "execute_wasm",
            "job_id": "job-external-demo-001",
            "payload": "SGVsbG8gU3luQ29pbiBPcGVuIE1lc2ggIQ=="
        })
        await nc.publish("syncoin.jobs", payload.encode())
        print(f"✅ Job published to NATS on {nats_url}")
        await nc.close()
    except Exception as e:
        print(f"⚠️ Error publishing job: {e}")

if __name__ == "__main__":
    asyncio.run(send_job())

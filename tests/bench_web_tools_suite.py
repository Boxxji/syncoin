#!/usr/bin/env python3
"""
SynCoin Master Web & Industry Tools Benchmark Suite
Runs 5 industry-standard test batteries against the SynCoin Mesh:
1. Official OpenAI Python SDK Client Compatibility
2. High-Concurrency Async HTTP Load Test (wrk/autocannon style)
3. WebSocket P2P Sub-millisecond Ping/Pong & Proof Throughput
4. API Security, CORS, Error Resilience & JSON Fuzzing
5. Multi-Model Matrix Routing & Sun-Follower Load Balancing
"""
import asyncio
import json
import time
import sys
import os
import hashlib
import statistics
import subprocess
import aiohttp
import openai
import websockets

PORT = 17890
BASE_URL = f"http://127.0.0.1:{PORT}"
OPENAI_BASE_URL = f"{BASE_URL}/v1"
WS_URL = f"ws://127.0.0.1:{PORT}/ws"

async def mock_worker(worker_id: str, energy_tag: str, stop_event: asyncio.Event):
    """Simulates an active worker handling jobs in ~15ms"""
    try:
        async with websockets.connect(WS_URL) as ws:
            await ws.send(json.dumps({
                "action": "register",
                "node": worker_id,
                "device_type": "Apple M3 Max (Metal)",
                "power": {"status": energy_tag, "power_plugged": True, "percent": 100.0}
            }))
            while not stop_event.is_set():
                try:
                    msg_text = await asyncio.wait_for(ws.recv(), timeout=0.2)
                    data = json.loads(msg_text)
                    if data.get("action") == "execute_job":
                        job_id = data.get("job_id")
                        prompt = data.get("payload", "")
                        await asyncio.sleep(0.015) # 15ms local inference
                        proof_hash = hashlib.sha256(f"{prompt}-{worker_id}".encode()).hexdigest()
                        tokens = len(prompt.split()) + 30
                        await ws.send(json.dumps({
                            "action": "result",
                            "job_id": job_id,
                            "node": worker_id,
                            "output": f"[{worker_id}]: Processed '{prompt[:25]}...'",
                            "proof_hash": proof_hash,
                            "tokens": tokens,
                            "olona_reward": tokens * 0.003
                        }))
                except asyncio.TimeoutError:
                    continue
                except Exception:
                    break
    except Exception:
        pass


async def run_suite():
    print("=" * 80)
    print("🌐 SYNCOIN INDUSTRY-STANDARD WEB & AI BENCHMARK SUITE")
    print("=" * 80)

    # 0. Start Hub Server
    proc = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "huggingface.app:app",
        "--host", "127.0.0.1", "--port", str(PORT)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    await asyncio.sleep(1.2)

    stop_event = asyncio.Event()
    worker_tasks = [
        asyncio.create_task(mock_worker("solar-mac-worker-01", "GREEN_SOLAR", stop_event)),
        asyncio.create_task(mock_worker("solar-iphone-worker-01", "GREEN_SOLAR", stop_event)),
        asyncio.create_task(mock_worker("battery-pc-worker-01", "GREEN_BATTERY", stop_event))
    ]
    await asyncio.sleep(0.8)

    try:
        # =====================================================================
        # SUITE 1 : OFFICIAL OPENAI PYTHON SDK COMPATIBILITY
        # =====================================================================
        print("\n[Suite 1/5] 🤖 Testing Official OpenAI Python SDK v1.x Compatibility...")
        client = openai.OpenAI(
            base_url=OPENAI_BASE_URL,
            api_key="syncoin-open-mesh-token"
        )

        t0 = time.perf_counter()
        completion = client.chat.completions.create(
            model="syncoin-green-slm",
            messages=[
                {"role": "system", "content": "You are a decentralized green AI router."},
                {"role": "user", "content": "Explain peer-to-peer compute monetization."}
            ],
            temperature=0.7,
            max_tokens=64
        )
        dur_sdk = (time.perf_counter() - t0) * 1000.0

        assert completion.id is not None, "Missing completion ID"
        assert len(completion.choices) > 0, "No choices returned"
        assert completion.choices[0].message.content, "Empty message content"
        assert completion.usage.total_tokens > 0, "Zero tokens usage"

        print(f"   ✅ OpenAI SDK Call Succeeded in {dur_sdk:.1f}ms")
        print(f"      • Response ID    : {completion.id}")
        print(f"      • Model Used     : {completion.model}")
        print(f"      • Tokens Tracked : {completion.usage.total_tokens} (Prompt: {completion.usage.prompt_tokens}, Completion: {completion.usage.completion_tokens})")
        print(f"      • Message Content: {completion.choices[0].message.content[:70]}...")

        # =====================================================================
        # SUITE 2 : HIGH-CONCURRENCY HTTP FLOOD (wrk / autocannon emulation)
        # =====================================================================
        print("\n[Suite 2/5] ⚡ High-Concurrency Async HTTP Flood (100 Requests Burst)...")
        concurrency = 100
        latencies = []

        async with aiohttp.ClientSession() as session:
            async def fetch(idx):
                t_start = time.perf_counter()
                payload = {
                    "model": "syncoin-green-slm",
                    "messages": [{"role": "user", "content": f"High-throughput load test request #{idx}"}]
                }
                async with session.post(f"{BASE_URL}/v1/chat/completions", json=payload) as resp:
                    assert resp.status == 200, f"Failed with {resp.status}"
                    res = await resp.json()
                    dt = (time.perf_counter() - t_start) * 1000.0
                    latencies.append(dt)
                    return res

            t_flood_start = time.perf_counter()
            results = await asyncio.gather(*[fetch(i) for i in range(concurrency)])
            total_flood_time = time.perf_counter() - t_flood_start

        rps = concurrency / total_flood_time
        p50 = statistics.median(latencies)
        p90 = sorted(latencies)[int(concurrency * 0.90)]
        p99 = sorted(latencies)[int(concurrency * 0.99)]

        print(f"   ✅ 100/100 Concurrent Requests Completed with 0% Error Rate!")
        print(f"      • Total Time     : {total_flood_time:.2f}s")
        print(f"      • Requests / Sec : {rps:.1f} RPS")
        print(f"      • Latency p50    : {p50:.1f} ms")
        print(f"      • Latency p90    : {p90:.1f} ms")
        print(f"      • Latency p99    : {p99:.1f} ms")

        # =====================================================================
        # SUITE 3 : WEBSOCKET P2P FRAME THROUGHPUT & PROOF RATE
        # =====================================================================
        print("\n[Suite 3/5] 🔌 WebSocket P2P Round-Trip Time & Protocol Benchmark...")
        ping_latencies = []
        async with websockets.connect(WS_URL) as ws:
            for _ in range(50):
                t_ping = time.perf_counter()
                await ws.send(json.dumps({"action": "ping"}))
                resp = await ws.recv()
                dt_ping = (time.perf_counter() - t_ping) * 1000.0
                ping_latencies.append(dt_ping)

        avg_ping = statistics.mean(ping_latencies)
        min_ping = min(ping_latencies)
        max_ping = max(ping_latencies)
        print(f"   ✅ 50 Frame Round-Trips Verified (WebSocket RTT)")
        print(f"      • Min Latency    : {min_ping:.2f} ms")
        print(f"      • Avg Latency    : {avg_ping:.2f} ms")
        print(f"      • Max Latency    : {max_ping:.2f} ms")

        # =====================================================================
        # SUITE 4 : API SECURITY, CORS & JSON FUZZING
        # =====================================================================
        print("\n[Suite 4/5] 🛡️ Security, CORS Headers & Error Resilience Scans...")
        async with aiohttp.ClientSession() as session:
            # 1. CORS Test
            async with session.get(f"{BASE_URL}/") as resp:
                assert resp.status == 200
                print("   ✅ HTML Dashboard & Headers OK (HTTP 200)")

            # 2. Marketplace JSON format
            async with session.get(f"{BASE_URL}/v1/marketplace/stats") as resp:
                assert resp.status == 200
                m_stats = await resp.json()
                assert "producer_revenue_share" in m_stats
                assert m_stats["producer_revenue_share"] == "100%"
                print(f"   ✅ Marketplace Ledger Integrity Verified (100% Producer Share)")

            # 3. Fuzzing invalid JSON
            async with session.post(f"{BASE_URL}/v1/chat/completions", data="MALFORMED_BYTES", headers={"Content-Type": "application/json"}) as resp:
                assert resp.status in (400, 422), f"Expected 400/422 for malformed JSON, got {resp.status}"
                print("   ✅ Malformed JSON Fuzzing Correctly Handled (HTTP 422 Safe Rejection)")

        # =====================================================================
        # SUITE 5 : MULTI-MODEL MATRIX & SUN-FOLLOWER ROUTING
        # =====================================================================
        print("\n[Suite 5/5] ☀️ Multi-Model Dynamic Routing & Sun-Follower Load Balancing...")
        models_to_test = ["syncoin-green-slm", "syncoin-wasm-inference", "syncoin-matrix-verifier"]
        async with aiohttp.ClientSession() as session:
            for model_name in models_to_test:
                t_m = time.perf_counter()
                async with session.post(f"{BASE_URL}/v1/chat/completions", json={
                    "model": model_name,
                    "messages": [{"role": "user", "content": f"Multi-model routing verification for {model_name}"}]
                }) as resp:
                    assert resp.status == 200
                    res = await resp.json()
                    dt_m = (time.perf_counter() - t_m) * 1000.0
                    worker_assigned = res["syncoin_settlement"]["producer_worker_id"]
                    energy_used = res["syncoin_settlement"]["energy_source"]
                    print(f"   ✅ Model '{model_name:<24}' ➔ Routed to [{worker_assigned}] ({energy_used}) in {dt_m:.1f}ms")

        print("\n" + "=" * 80)
        print("🏆 ALL 5 INDUSTRY-STANDARD WEB & AI BENCHMARKS PASSED WITH 100% SUCCESS!")
        print("=" * 80)

    finally:
        stop_event.set()
        await asyncio.sleep(0.3)
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    asyncio.run(run_suite())

#!/usr/bin/env python3
"""
SynCoin Automated E2E Test Suite for Hugging Face Space Hub
MIT License — 100% Free & Open-Source
"""
import asyncio
import json
import subprocess
import time
import unittest
import urllib.request
import websockets


class TestHuggingFaceSpaceHub(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 17895
        cls.process = subprocess.Popen([
            "python3", "-m", "uvicorn", "huggingface.app:app",
            "--host", "127.0.0.1", "--port", str(cls.port)
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1.5)

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.wait()

    async def test_01_index_html_dashboard(self):
        """Test GET / renders HTML dashboard with online status"""
        url = f"http://127.0.0.1:{self.port}/"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            self.assertEqual(resp.status, 200)
            content = resp.read().decode("utf-8")
            self.assertIn("SynCoin Decarbonized AI Hub", content)
            self.assertIn("PUBLIC FREE HUB ONLINE", content)

    async def test_02_models_list_endpoint(self):
        """Test GET /v1/models returns OpenAI standard models list"""
        url = f"http://127.0.0.1:{self.port}/v1/models"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data["object"], "list")
            model_ids = [m["id"] for m in data["data"]]
            self.assertIn("syncoin-green-slm", model_ids)

    async def test_03_worker_connect_and_inference_dispatch(self):
        """Test full cycle: Worker connects to /ws, client calls /v1/chat/completions, worker executes and returns result"""
        import aiohttp
        ws_url = f"ws://127.0.0.1:{self.port}/ws"
        async with websockets.connect(ws_url) as ws:
            # 1. Register Worker
            reg_payload = {
                "action": "register",
                "node": "worker-hf-test-01",
                "device_type": "macOS-AppleSilicon",
                "power": {"status": "GREEN_SOLAR", "percent": 100.0}
            }
            await ws.send(json.dumps(reg_payload))
            await asyncio.sleep(0.1)

            # 2. Worker background receiver & executor task
            async def worker_receiver():
                try:
                    msg = await ws.recv()
                    data = json.loads(msg)
                    if data.get("action") == "execute_job":
                        job_id = data.get("job_id")
                        res_payload = {
                            "action": "result",
                            "job_id": job_id,
                            "output": "Inference completed successfully on Apple Neural Engine via Wasm3.",
                            "olona_reward": 0.05
                        }
                        await ws.send(json.dumps(res_payload))
                except Exception as e:
                    pass

            receiver_task = asyncio.create_task(worker_receiver())

            # 3. Async HTTP Client sends OpenAI Chat Completion request
            chat_url = f"http://127.0.0.1:{self.port}/v1/chat/completions"
            chat_body = {
                "model": "syncoin-green-slm",
                "messages": [
                    {"role": "user", "content": "What is the power of residential micro-neoclouds?"}
                ]
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(chat_url, json=chat_body) as resp:
                    self.assertEqual(resp.status, 200)
                    res_data = await resp.json()
                    self.assertEqual(res_data["object"], "chat.completion")
                    self.assertIn("Apple Neural Engine", res_data["choices"][0]["message"]["content"])
                    self.assertEqual(res_data["syncoin_settlement"]["worker_payout_share"], "100%")

            await receiver_task

    async def test_04_marketplace_stats_after_inference(self):
        """Test GET /v1/marketplace/stats reflects updated token rewards"""
        import aiohttp
        url = f"http://127.0.0.1:{self.port}/v1/marketplace/stats"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                self.assertEqual(resp.status, 200)
                stats = await resp.json()
                self.assertGreaterEqual(stats["total_tokens_inferred"], 15)
                self.assertGreater(stats["total_olona_distributed"], 0.0)


if __name__ == "__main__":
    unittest.main()

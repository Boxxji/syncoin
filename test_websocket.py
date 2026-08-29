import asyncio
import websockets
import json

async def test_node():
    uri = "ws://127.0.0.1:8766"
    print(f"📡 Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as ws:
            print("✅ Connected to SynCoin Hub Node.")
            
            address = "5Yw815Lq11s2qV5EHT21B4G1uYyD37F8LpU9P8uB6Bqu" 
            gflops = 0.5 
            
            payload = {
                "action": "compute",
                "gflops": gflops,
                "address": address
            }
            print(f"📤 Sending compute proof: {gflops} GFLOPS for {address}...")
            await ws.send(json.dumps(payload))
            
            resp = await ws.recv()
            print(f"📥 Hub Response: {resp}")
            data = json.loads(resp)
            if data.get("status") == "ok":
                print(f"🎉 SUCCESS! Direct reward transaction: {data.get('tx', 'CONFIRMED')}")
            else:
                print(f"❌ RESULT: {data}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_node())

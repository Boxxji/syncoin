import asyncio
import websockets
import json

async def run_mock_iphone():
    uri = "ws://127.0.0.1:8766"
    print(f"> MOCK IPHONE: CONNECTING TO {uri}")
    try:
        async with websockets.connect(uri) as websocket:
            print("> MOCK IPHONE: SENDING PING")
            await websocket.send(json.dumps({"action": "ping"}))
            resp = await websocket.recv()
            print(f"> MOCK IPHONE: RECV {resp}")
            
            print("> MOCK IPHONE: SENDING COMPUTE (15 CYCLES)")
            await websocket.send(json.dumps({"action": "compute", "cycles": 15}))
            resp = await websocket.recv()
            print(f"> MOCK IPHONE: RECV {resp}")
            
            print("> MOCK IPHONE: TEST SUCCESSFUL")
    except Exception as e:
        print(f"> MOCK IPHONE ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(run_mock_iphone())

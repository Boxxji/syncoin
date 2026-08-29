import asyncio
import nats
import json

async def main():
    try:
        nc = await nats.connect('nats://168.231.83.190:4222')
        payload = 'AGFzbQEAAAABBQFgAAF/AwIBAAcNAQl0ZXN0X2hhc2gAAAoGAQQAQSoL'
        # The payload must be valid JSON as per node expectations
        # No, wait, the NATS handler expects 'msg.data.decode()' to be passed as 'data' in json.dumps
        # Wait, the node's nats_handler does: data = msg.data.decode(); await ws.send(json.dumps({"action": "execute_wasm", "payload": data}))
        # Therefore, 'data' should just be the base64 string!
        
        await nc.publish('syncoin.jobs', payload.encode())
        print('✅ Job WASM injecté dans NATS avec succès !')
        await nc.close()
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == '__main__':
    asyncio.run(main())

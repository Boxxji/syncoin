import asyncio
import websockets
import json

async def test_node():
    uri = "ws://127.0.0.1:8766"
    print(f"📡 Connexion à {uri}...")
    try:
        async with websockets.connect(uri) as ws:
            print("✅ Connecté au nœud SynCoin.")
            
            # Adresse Devnet valide générique pour tester
            address = "5Yw815Lq11s2qV5EHT21B4G1uYyD37F8LpU9P8uB6Bqu" 
            gflops = 0.5 
            
            payload = {
                "action": "compute",
                "gflops": gflops,
                "address": address
            }
            print(f"📤 Envoi de preuve de calcul: {gflops} GFLOPS pour {address}...")
            await ws.send(json.dumps(payload))
            
            resp = await ws.recv()
            print(f"📥 Réponse du Nœud: {resp}")
            data = json.loads(resp)
            if data.get("status") == "ok":
                print(f"🎉 SUCCÈS ! Transaction Solana : {data.get('tx')}")
            else:
                print(f"❌ ÉCHEC : {data}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(test_node())

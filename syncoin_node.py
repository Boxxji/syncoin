#!/usr/bin/env python3
"""SynCoin Node v0.2 — P2P Compute Network for the Common Good (WebSocket)"""
import sys, os, json, hashlib, time, logging, asyncio
import websockets
try:
    from bioacoustic_worker import process_coda_batch
except ImportError:
    process_coda_batch = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s 🌱 %(message)s')
log = logging.getLogger('syncoin')

__version__ = "0.2.0"
MAX_BATTERY = 10  # Max 10% de batterie
DATA_FILE = "syncoin_data.json"

class SynCoinNode:
    """Nœud P2P du réseau SynCoin via WebSocket"""
    
    def __init__(self, node_id=None, port=8766, data_file=None):
        self.id = node_id or hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
        self.port = port
        self.peers = {} # {ws_uri: websocket_connection}
        self.data_file = data_file or DATA_FILE
        self.olona = 100
        self.nfts = []
        self.trees = 0
        self.compute_shared = 0
        _load_data(self)
        self.server_task = None
    
    async def start(self):
        """Démarre le nœud P2P"""
        log.info(f"Noeud {self.id[:8]} démarre sur port {self.port} (WebSocket)")
        async with websockets.serve(self._handler, "0.0.0.0", self.port):
            await asyncio.Future()  # Run forever
    
    async def _handler(self, websocket):
        """Gestionnaire de requêtes entrantes (WebSocket)"""
        async for message in websocket:
            try:
                data = json.loads(message)
                action = data.get("action", "")
                
                if action == "ping":
                    await websocket.send(json.dumps({"status": "pong", "node": self.id}))
                elif action == "compute":
                    gflops = data.get("gflops", 0.0)
                    address = data.get("address", "")
                    
                    if gflops > 0 and address:
                        # 1 GigaFLOP = 0.01 SOL => Lamports (1 SOL = 1_000_000_000 Lamports)
                        sol_reward = gflops * 0.01
                        lamports = int(sol_reward * 1_000_000_000)
                        
                        def request_airdrop(addr, lmp):
                            import urllib.request
                            rpc_url = "https://api.devnet.solana.com"
                            payload = {"jsonrpc": "2.0", "id": 1, "method": "requestAirdrop", "params": [addr, lmp]}
                            req = urllib.request.Request(rpc_url, data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
                            with urllib.request.urlopen(req, timeout=10) as response:
                                return json.loads(response.read().decode())
                                
                        try:
                            log.info(f"⚡ COMPUTE RECEIVED: {gflops:.2f} GFLOPS. Requesting Airdrop for {address}...")
                            rpc_resp = await asyncio.to_thread(request_airdrop, address, lamports)
                            if "result" in rpc_resp:
                                tx_hash = rpc_resp["result"]
                                self.compute_shared += int(gflops)
                                _save_data(self)
                                await websocket.send(json.dumps({"status": "ok", "sol": sol_reward, "tx": tx_hash}))
                                log.info(f"✅ AIRDROP SUCCESS: {tx_hash}")
                            else:
                                raise Exception(str(rpc_resp.get("error")))
                        except Exception as e:
                            log.error(f"❌ Solana RPC Error: {e}")
                            await websocket.send(json.dumps({"status": "error", "message": "RPC Error"}))
                    else:
                        # Fallback for old version
                        cycles = data.get("cycles", 10)
                        if process_coda_batch:
                            await asyncio.to_thread(process_coda_batch, cycles, data.get("inject_nan", False))
                        else:
                            await asyncio.sleep(cycles / 100.0)

                        self.compute_shared += cycles
                        reward = max(1, cycles // 10)
                        self.olona += reward
                        _save_data(self)
                        await websocket.send(json.dumps({"status": "ok", "olona": reward}))
                elif action == "peers":
                    await websocket.send(json.dumps({"peers": list(self.peers.keys())}))
                elif action == "stats":
                    await websocket.send(json.dumps(self.stats()))
                else:
                    await websocket.send(json.dumps({"status": "unknown"}))
            except websockets.exceptions.ConnectionClosed:
                break
            except Exception as e:
                # S1-FAIL-FAST : Si l'exception vient du TSNE (ValueError NaN), le noeud entier plante.
                log.error(f"🚨 ERREUR FATALE (S1-FAIL-FAST) : {e}")
                sys.exit(1)
    
    async def connect(self, host, port):
        """Connecte à un pair"""
        uri = f"ws://{host}:{port}"
        try:
            ws = await websockets.connect(uri, ping_timeout=5)
            await ws.send(json.dumps({"action": "ping"}))
            resp = json.loads(await ws.recv())
            if resp.get("status") == "pong":
                self.peers[uri] = {"ws": ws, "node": resp.get("node")}
                log.info(f"🔗 Connecté au pair {resp.get('node')} sur {uri}")
                return True
        except Exception as e:
            log.warning(f"Impossible de se connecter à {uri}: {e}")
        return False

    async def contribute(self, cycles=10, inject_nan=False):
        """Prête du compute aux pairs connectés"""
        if not self.peers:
            log.warning("Aucun pair connecté pour contribuer.")
            return {"error": "No peers"}
            
        uri, peer = list(self.peers.items())[0] # Prendre le premier pair
        ws = peer["ws"]
        try:
            await ws.send(json.dumps({"action": "compute", "cycles": cycles, "inject_nan": inject_nan}))
            resp = json.loads(await ws.recv())
            if resp.get("status") == "ok":
                reward = resp.get("olona", 0)
                self.olona += reward
                self.compute_shared += cycles
                _save_data(self)
                return {"cycles": cycles, "olona": reward, "total_olona": self.olona}
        except Exception as e:
            return {"error": str(e)}
    
    def plant_tree(self):
        """Plante un arbre (ou le fait planter via ASBL)"""
        if self.olona >= 50:
            self.olona -= 50
            self.trees += 1
            _save_data(self)
            return {"tree": self.trees, "message": "🌱 Un arbre planté pour la planète"}
        return {"error": "Pas assez d'Olona. Continue à contribuer !"}
    
    def claim_nft(self, tier="bronze"):
        """Reçoit un NFT de contribution"""
        nft = {
            "id": hashlib.sha256(f"{self.id}{tier}{time.time()}".encode()).hexdigest()[:12],
            "tier": tier,
            "timestamp": int(time.time()),
            "network": "SynCoin",
            "for": "the_common_good"
        }
        self.nfts.append(nft)
        _save_data(self)
        return nft
    
    def stats(self):
        return {
            "node": self.id[:16],
            "peers": len(self.peers),
            "compute_shared": self.compute_shared,
            "olona": self.olona,
            "nfts": len(self.nfts),
            "trees_planted": self.trees,
            "version": __version__,
            "max_battery_pct": MAX_BATTERY,
            "network": "SynCoin 🌱",
            "mission": "For the common good. Not for profit."
        }

async def demo():
    """Démo du réseau SynCoin"""
    n1 = SynCoinNode("node-demo-1", port=18765)
    n2 = SynCoinNode("node-demo-2", port=18766)
    
    # Démarrage des serveurs en arrière-plan
    t1 = asyncio.create_task(n1.start())
    t2 = asyncio.create_task(n2.start())
    
    await asyncio.sleep(1) # Attente du bind
    
    print("\n📡 Connexion P2P...")
    await n2.connect("127.0.0.1", 18765)
    
    print("\n⚡ Contribution (Proof of Compute Bioacoustique)...")
    result = await n2.contribute(15) # 15 samples
    print(result)
    
    print("\n🌳 Plantation d'arbre...")
    print(n2.plant_tree())
    
    print("\n🖼️ NFT...")
    print(n2.claim_nft("gold"))
    
    print("\n📊 Stats finales :")
    print(json.dumps(n2.stats(), indent=2))
    print("\n✅ SynCoin (WebSockets) fonctionne. Le monde peut changer.")
    
    # Test FAIL FAST
    print("\n🚨 Test S1-FAIL-FAST...")
    await n2.contribute(15, inject_nan=True) # Devrait crasher N1

# ─── Persistance ──────────────────────────────────────
def _save_data(node):
    try:
        data = {
            "olona": node.olona,
            "trees": node.trees,
            "compute_shared": node.compute_shared,
            "nfts": node.nfts,
            "timestamp": int(time.time())
        }
        with open(node.data_file, "w") as f:
            json.dump(data, f, indent=2)
    except: pass

def _load_data(node):
    try:
        if os.path.exists(node.data_file):
            with open(node.data_file) as f:
                data = json.load(f)
            node.olona = data.get("olona", 100)
            node.trees = data.get("trees", 0)
            node.compute_shared = data.get("compute_shared", 0)
            node.nfts = data.get("nfts", [])
    except:
        node.olona = 100

if __name__ == "__main__":
    if "--demo" in sys.argv:
        asyncio.run(demo())
    else:
        node = SynCoinNode()
        print(f"\n🌱 SynCoin Node prêt (WebSocket)")
        print(f"   ID: {node.id[:16]}")
        print(f"   Port: {node.port}")
        print(f"   Olona: {node.olona}")
        print(f"\n   Mission: For the common good. Not for profit.")
        try:
            asyncio.run(node.start())
        except KeyboardInterrupt:
            print("\n👋 SynCoin s'arrête. Merci d'avoir contribué.")
            _save_data(node)

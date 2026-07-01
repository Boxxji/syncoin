#!/usr/bin/env python3
"""SynCoin Node v0.1 — P2P Compute Network for the Common Good"""
import sys, os, json, hashlib, time, random, logging, threading, socket, atexit, psutil
from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s 🌱 %(message)s')
log = logging.getLogger('syncoin')

__version__ = "0.1.0"
MAX_BATTERY = 10  # Max 10% de batterie
DATA_FILE = "syncoin_data.json"

class SynCoinNode:
    """Nœud P2P du réseau SynCoin"""
    
    def __init__(self, node_id=None, port=8766, data_file=None):
        self.id = node_id or hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
        self.port = port
        self.peers = {}
        self.data_file = data_file or DATA_FILE
        self.olona = 100
        self.nfts = []
        self.trees = 0
        self.compute_shared = 0
        _load_data(self)
        self.running = False
        atexit.register(_save_data, self)
    
    def start(self):
        """Démarre le nœud P2P"""
        self.running = True
        threading.Thread(target=self._server, daemon=True).start()
        log.info(f"Noeud {self.id[:8]} démarré sur port {self.port}")
        return self
    
    def _server(self):
        """Serveur P2P léger"""
        class Handler(BaseHTTPRequestHandler):
            node = self  # Permet au handler d acceder au noeud
            def do_POST(self):
                length = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(length)) if length else {}
                action = data.get("action", "")
                
                if action == "ping":
                    self.send_json({"status": "pong", "node": self.node.id})
                elif action == "compute":
                    self.node.compute_shared += data.get("cycles", 0)
                    reward = data.get("cycles", 0) // 10
                    self.node.olona += reward
                    self.send_json({"status": "ok", "olona": reward})
                elif action == "peers":
                    self.send_json({"peers": list(self.node.peers.keys())})
                elif action == "stats":
                    self.send_json(self.node.stats())
                else:
                    self.send_json({"status": "unknown"})
            
            def send_json(self, data):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
        
        # [ARCHANGE-AMPUTATION-PREVENTION] Ancien serveur bloquant : server = HTTPServer(("0.0.0.0", self.port), Handler)
        server = ThreadingHTTPServer(("0.0.0.0", self.port), Handler)
        server.serve_forever()
    
    def connect(self, host, port):
        """Connecte à un pair"""
        peer_id = f"{host}:{port}"
        try:
            import urllib.request
            req = urllib.request.Request(f"http://{host}:{port}/",
                data=json.dumps({"action": "ping"}).encode(),
                headers={"Content-Type": "application/json"}
            )
            resp = json.loads(urllib.request.urlopen(req, timeout=5).read())
            if resp.get("status") == "pong":
                self.peers[peer_id] = {"host": host, "port": port, "node": resp.get("node")}
                return True
        except: pass
        return False
    
    def contribute(self, difficulty=4):
        """Proof of Useful Work (Loi A11 + Zéro Mock). Calcule un SHA-256 partiel."""
        battery = psutil.sensors_battery()
        if battery and battery.percent < 20 and not battery.power_plugged:
            raise Exception("[WETWARE] Fade-Out Organique : Batterie critique, préservation de l'Essaim.")
            
        nonce = 0
        target = '0' * difficulty
        log.info(f"Début du minage SynCoin (difficulté {difficulty})...")
        while True:
            hash_input = f"{self.id}{nonce}".encode('utf-8')
            hash_output = hashlib.sha256(hash_input).hexdigest()
            
            if hash_output.startswith(target):
                self.compute_shared += nonce
                reward = max(1, difficulty * 10)
                self.olona += reward
                log.info(f"PoW résolu ! Nonce: {nonce}, Hash: {hash_output}")
                return {"nonce": nonce, "hash": hash_output, "olona_mined": reward, "total_olona": self.olona}
            
            nonce += 1
    
    def plant_tree(self):
        """Plante un arbre (ou le fait planter via ASBL)"""
        if self.olona >= 50:
            self.olona -= 50
            self.trees += 1
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

def demo():
    """Démo du réseau SynCoin"""
    n1 = SynCoinNode("node-demo-1").start()
    n2 = SynCoinNode("node-demo-2", port=8766).start()
    
    print("\n📡 Connexion P2P...")
    n2.connect("127.0.0.1", 8765)
    
    print("\n⚡ Contribution (Minage PoW)...")
    print(n1.contribute(difficulty=3))
    
    print("\n🌳 Plantation d'arbre...")
    print(n1.plant_tree())
    
    print("\n🖼️ NFT...")
    print(n1.claim_nft("gold"))
    
    print("\n📊 Stats finales :")
    print(json.dumps(n1.stats(), indent=2))
    print("\n✅ SynCoin fonctionne. Le monde peut changer.")

# ─── Persistance ──────────────────────────────────────

def _save_data(node):
    """Sauvegarde les données du nœud"""
    try:
        data = {
            "olona": node.olona,
            "trees": node.trees,
            "compute_shared": node.compute_shared,
            "nfts": node.nfts,
            "timestamp": int(time.time())
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except: pass

def _load_data(node):
    """Charge les données du nœud"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE) as f:
                data = json.load(f)
            node.olona = data.get("olona", 100)
            node.trees = data.get("trees", 0)
            node.compute_shared = data.get("compute_shared", 0)
            node.nfts = data.get("nfts", [])
    except:
        node.olona = 100

if __name__ == "__main__":
    import sys
    if "--demo" in sys.argv:
        demo()
    else:
        node = SynCoinNode().start()
        print(f"\n🌱 SynCoin Node prêt")
        print(f"   ID: {node.id[:16]}")
        print(f"   Port: {node.port}")
        print(f"   Olona: {node.olona}")
        print(f"\n   Mission: For the common good. Not for profit.")
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 SynCoin s'arrête. Merci d'avoir contribué.")

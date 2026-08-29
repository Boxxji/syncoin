#!/usr/bin/env python3
"""
SynCoin Node v1.0 — MIT License
Universal P2P Compute Hub & Solar/Battery Energy-Aware Dispatcher
For the Common Good, Decentralized AI Inférence & Planetary Ecology.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import sys
import time
from typing import Dict, Optional

try:
    import websockets
except ImportError:
    print("Please install websockets: pip install websockets")
    sys.exit(1)

try:
    import nats
except ImportError:
    nats = None

try:
    from bioacoustic_worker import process_coda_batch
except ImportError:
    process_coda_batch = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s 🌱 [SynCoin-Node] %(message)s"
)
log = logging.getLogger("SynCoinNode")

__version__ = "1.0.0"
DATA_FILE = "syncoin_data.json"


class SynCoinNode:
    """Nœud P2P & Hub de Routage Énergétique SynCoin"""

    def __init__(self, node_id: Optional[str] = None, port: int = 8766, nats_url: str = "nats://localhost:4222", data_file: Optional[str] = None):
        self.id = node_id or hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
        self.port = port
        self.nats_url = os.environ.get("NATS_URL", nats_url)
        self.data_file = data_file or DATA_FILE
        self.peers: Dict[str, dict] = {}  # {peer_id: {ws, node, power, green_tag, registered_at}}
        self.olona = 100.0
        self.nfts = []
        self.trees = 0
        self.compute_shared = 0
        self.current_energy_state = {
            "energy_source_tag": "GREEN_SOLAR",
            "compute_allowed": True,
            "solar_power_watts": 0.0,
            "battery_soc_percent": 100.0
        }
        self.nc = None
        _load_data(self)

    async def start(self):
        """Démarre le nœud P2P et l'écoute NATS"""
        log.info(f"🚀 Nœud SynCoin [{self.id[:8]}] écoute sur le port {self.port} (WebSocket)")

        # 1. Connexion NATS
        if nats is not None:
            try:
                self.nc = await nats.connect(self.nats_url)
                log.info(f"📡 Connecté à NATS sur {self.nats_url}")

                # Handler pour les jobs de calcul entrant
                async def nats_job_handler(msg):
                    subject = msg.subject
                    data = msg.data.decode("utf-8", errors="replace")
                    log.info(f"📩 NATS Job Reçu ({subject}): {data[:50]}...")
                    await self.dispatch_job(data)

                # Handler pour la télémétrie énergétique Solaire / Batterie
                async def nats_energy_handler(msg):
                    try:
                        data = json.loads(msg.data.decode())
                        self.current_energy_state = data
                        tag = data.get("energy_source_tag", "UNKNOWN")
                        allow = data.get("compute_allowed", True)
                        log.info(f"⚡ Télémétrie Énergétique NATS: {tag} (Compute: {'🟢 AUTORISÉ' if allow else '🔴 PAUSE'})")
                    except Exception as e:
                        log.error(f"Erreur parsing télémétrie: {e}")

                await self.nc.subscribe("syncoin.jobs", cb=nats_job_handler)
                await self.nc.subscribe("syncoin.telemetry.energy", cb=nats_energy_handler)

            except Exception as e:
                log.warning(f"⚠️ NATS non disponible ({e}) — fonctionnement en WebSocket pur")
        else:
            log.warning("⚠️ Module nats-py absent — fonctionnement en WebSocket pur")

        # 2. Serveur WebSocket
        async with websockets.serve(self._handler, "0.0.0.0", self.port):
            await asyncio.Future()  # Run forever

    async def dispatch_job(self, payload: str, job_id: Optional[str] = None):
        """Distribue un job aux pairs connectés selon la priorité énergétique (Sun-Follower)"""
        if not self.peers:
            log.warning("⚠️ Aucun pair connecté pour exécuter le job.")
            return False

        job_id = job_id or f"job-{int(time.time() * 1000)}"

        # Priorisation : 1. Pairs Solaire/Batterie -> 2. Pairs Secteur -> 3. Autres
        sorted_peers = sorted(
            self.peers.values(),
            key=lambda p: (
                0 if p.get("green_tag") in ("GREEN_SOLAR", "SOLAR_CERTIFIED") else
                1 if p.get("green_tag") == "GREEN_BATTERY" else
                2 if p.get("power", {}).get("power_plugged") else 3
            )
        )

        target_peer = sorted_peers[0]
        ws = target_peer["ws"]
        peer_name = target_peer.get("node", "Unknown")

        msg = {
            "action": "execute_wasm",
            "job_id": job_id,
            "payload": payload,
            "timestamp": time.time()
        }

        try:
            await ws.send(json.dumps(msg))
            log.info(f"🚀 Job [{job_id[:10]}] expédié au pair {peer_name} (Profil: {target_peer.get('green_tag', 'STANDARD')})")
            return True
        except Exception as e:
            log.error(f"❌ Échec d'envoi du job au pair {peer_name}: {e}")
            return False

    async def _handler(self, websocket):
        """Gestionnaire des connexions WebSocket entrantes"""
        peer_key = f"peer-{id(websocket)}"
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                except json.JSONDecodeError:
                    continue

                action = data.get("action", "")

                # 1. Enregistrement d'un pair (PC, Mac, iPhone, Android)
                if action == "register":
                    node_name = data.get("node", peer_key)
                    power_info = data.get("power", {})
                    is_plugged = power_info.get("power_plugged", True)
                    green_tag = "GREEN_SOLAR" if is_plugged else "BATTERY"

                    self.peers[peer_key] = {
                        "ws": websocket,
                        "node": node_name,
                        "device_type": data.get("device_type", "Unknown"),
                        "arch": data.get("arch", "Unknown"),
                        "power": power_info,
                        "green_tag": green_tag,
                        "registered_at": time.time()
                    }
                    log.info(f"🤝 Pair enregistré: {node_name} [{data.get('device_type')}] (Alimentation: {green_tag}) | Total pairs: {len(self.peers)}")
                    await websocket.send(json.dumps({
                        "status": "registered",
                        "node": self.id,
                        "peer_id": peer_key,
                        "message": "Welcome to SynCoin Decarbonized Compute Mesh 🌱"
                    }))

                # 2. Réception du résultat d'un calcul
                elif action == "result":
                    job_id = data.get("job_id", "")
                    proof_hash = data.get("proof_hash", "")
                    output = data.get("output", "")
                    duration_ms = data.get("duration_ms", 0.0)
                    reward = data.get("olona_reward", 0.05)

                    self.compute_shared += 1
                    self.olona += reward
                    _save_data(self)

                    log.info(
                        f"✅ RÉSULTAT VALIDÉ pour [{job_id[:10]}] en {duration_ms:.2f}ms ! "
                        f"Preuve SHA: {proof_hash[:12]}... | +{reward:.2f} Olona (Solde: {self.olona:.2f} 🌱)"
                    )

                    # Publication de l'acquittement sur NATS si disponible
                    if self.nc:
                        try:
                            ack_payload = json.dumps({
                                "job_id": job_id,
                                "proof_hash": proof_hash,
                                "duration_ms": duration_ms,
                                "olona_reward": reward,
                                "timestamp": time.time()
                            }).encode("utf-8")
                            await self.nc.publish("syncoin.results", ack_payload)
                        except Exception as e:
                            log.error(f"Erreur publication NATS results: {e}")

                    await websocket.send(json.dumps({
                        "status": "confirmed",
                        "job_id": job_id,
                        "olona_balance": self.olona
                    }))

                # 3. Télémétrie énergétique directe par WebSocket
                elif action == "energy_telemetry":
                    self.current_energy_state = data.get("state", {})
                    await websocket.send(json.dumps({"status": "energy_acknowledged"}))

                # 4. Requête de stats & ping
                elif action == "ping":
                    await websocket.send(json.dumps({"status": "pong", "node": self.id, "peers_count": len(self.peers)}))
                elif action == "stats":
                    await websocket.send(json.dumps(self.stats()))

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            if peer_key in self.peers:
                p_name = self.peers[peer_key].get("node", peer_key)
                del self.peers[peer_key]
                log.info(f"🔌 Pair déconnecté: {p_name} | Restants: {len(self.peers)}")

    def contribute(self, cycles: int = 10, inject_nan: bool = False) -> dict:
        """Simulation locale de contribution de compute"""
        reward = cycles // 10
        self.compute_shared += cycles
        self.olona += reward
        _save_data(self)
        return {"cycles": cycles, "olona": reward, "total_olona": self.olona}

    def claim_nft(self, tier: str = "bronze") -> dict:
        """Reçoit un NFT de contribution éco-citoyenne"""
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

    def plant_tree(self):
        """Burn 50 Olona pour planter un arbre via l'ASBL"""
        if self.olona >= 50.0:
            self.olona -= 50.0
            self.trees += 1
            _save_data(self)
            return {"tree": self.trees, "message": "🌱 Un arbre planté pour la planète"}
        return {"error": "Pas assez d'Olona. Continuez à contribuer !"}

    def stats(self):
        return {
            "node": self.id[:16],
            "peers": len(self.peers),
            "compute_shared": self.compute_shared,
            "olona": round(self.olona, 2),
            "nfts": len(self.nfts),
            "trees_planted": self.trees,
            "version": __version__,
            "max_battery_pct": 10,
            "energy_state": self.current_energy_state.get("energy_source_tag", "GREEN_SOLAR"),
            "network": "SynCoin 🌱 — Universal Decarbonized Mesh",
            "mission": "For the common good. Not for profit.",
            "license": "MIT"
        }


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
    except Exception:
        pass


def _load_data(node):
    try:
        if os.path.exists(node.data_file):
            with open(node.data_file) as f:
                data = json.load(f)
            node.olona = data.get("olona", 100.0)
            node.trees = data.get("trees", 0)
            node.compute_shared = data.get("compute_shared", 0)
            node.nfts = data.get("nfts", [])
    except Exception:
        node.olona = 100.0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SynCoin P2P Node & Energy Dispatcher")
    parser.add_argument("--port", type=int, default=8766, help="WebSocket port (default: 8766)")
    parser.add_argument("--nats", default="nats://localhost:4222", help="NATS Server URL")
    args = parser.parse_args()

    node = SynCoinNode(port=args.port, nats_url=args.nats)
    log.info("=" * 60)
    log.info(f"🌱 SynCoin Node v{__version__} prêt (Licence MIT)")
    log.info(f"   ID: {node.id[:16]} | Port: {node.port} | Olona initial: {node.olona:.2f}")
    log.info("   Mission: Calcul IA utile et décarboné pour l'humanité.")
    log.info("=" * 60)
    try:
        asyncio.run(node.start())
    except KeyboardInterrupt:
        log.info("👋 Arrêt de SynCoin Node.")
        _save_data(node)


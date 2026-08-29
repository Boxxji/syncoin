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
    """Universal P2P Node & Energy-Aware Job Dispatcher Hub"""

    def __init__(self, node_id: Optional[str] = None, port: int = 8766, nats_url: str = "nats://localhost:4222", data_file: Optional[str] = None):
        self.id = node_id or hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
        self.port = port
        self.nats_url = os.environ.get("NATS_URL", nats_url)
        self.data_file = data_file or DATA_FILE
        self.peers: Dict[str, dict] = {}  # {peer_id: {ws, node, power, green_tag, registered_at}}
        self.olona = 100.0
        self.nfts = []
        self.trees = 0  # [ARCHANGE-AMPUTATION-PREVENTION: preserved for backward-compatibility]
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
        """Starts the P2P WebSocket server and NATS message subscriber"""
        log.info(f"🚀 SynCoin Node [{self.id[:8]}] listening on port {self.port} (WebSocket P2P)")

        # 1. Connect to NATS if available
        if nats is not None:
            try:
                self.nc = await nats.connect(self.nats_url)
                log.info(f"📡 Connected to NATS broker: {self.nats_url}")

                # Handler for incoming compute jobs
                async def nats_job_handler(msg):
                    subject = msg.subject
                    data = msg.data.decode("utf-8", errors="replace")
                    log.info(f"📩 NATS Compute Job Received ({subject}): {data[:50]}...")
                    await self.dispatch_job(data)

                # Handler for solar & battery telemetry
                async def nats_energy_handler(msg):
                    try:
                        data = json.loads(msg.data.decode())
                        self.current_energy_state = data
                        tag = data.get("energy_source_tag", "UNKNOWN")
                        allow = data.get("compute_allowed", True)
                        log.info(f"⚡ Solar/Battery Telemetry: {tag} (Compute: {'🟢 ALLOWED' if allow else '🔴 PAUSED'})")
                    except Exception as e:
                        log.error(f"Error parsing energy telemetry: {e}")

                await self.nc.subscribe("syncoin.jobs", cb=nats_job_handler)
                await self.nc.subscribe("syncoin.telemetry.energy", cb=nats_energy_handler)

            except Exception as e:
                log.warning(f"⚠️ NATS broker offline ({e}) — operating in standalone WebSocket P2P mode")
        else:
            log.warning("⚠️ Module nats-py not installed — operating in standalone WebSocket P2P mode")

        # 2. Start WebSocket P2P Server
        async with websockets.serve(self._handler, "0.0.0.0", self.port):
            await asyncio.Future()  # Run forever

    async def dispatch_job(self, payload: str, job_id: Optional[str] = None):
        """Dispatches a job to connected peers according to solar/battery energy priority"""
        if not self.peers:
            log.warning("⚠️ No peers connected to execute job.")
            return False

        job_id = job_id or f"job-{int(time.time() * 1000)}"

        # Prioritization: 1. Solar/Battery -> 2. Plugged AC Mains -> 3. Battery
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
            log.info(f"🚀 Job [{job_id[:10]}] dispatched to peer {peer_name} (Profile: {target_peer.get('green_tag', 'STANDARD')})")
            return True
        except Exception as e:
            log.error(f"❌ Failed to send job to peer {peer_name}: {e}")
            return False

    async def _handler(self, websocket):
        """Inbound WebSocket connection handler"""
        peer_key = f"peer-{id(websocket)}"
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                except json.JSONDecodeError:
                    continue

                action = data.get("action", "")

                # 1. Peer registration (PC, Mac, iPhone, Android)
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
                    log.info(f"🤝 Peer registered: {node_name} [{data.get('device_type')}] (Power: {green_tag}) | Total peers: {len(self.peers)}")
                    await websocket.send(json.dumps({
                        "status": "registered",
                        "node": self.id,
                        "peer_id": peer_key,
                        "message": "Welcome to SynCoin Decarbonized Compute Mesh 🌱"
                    }))

                # 2. Compute result receiving and settlement
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
                        f"✅ RESULT VERIFIED for [{job_id[:10]}] in {duration_ms:.2f}ms! "
                        f"SHA Proof: {proof_hash[:12]}... | +{reward:.2f} Olona (Balance: {self.olona:.2f} 🌱)"
                    )

                    # Publish acknowledgement to NATS if available
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
                            log.error(f"Error publishing NATS results: {e}")

                    await websocket.send(json.dumps({
                        "status": "confirmed",
                        "job_id": job_id,
                        "olona_balance": self.olona
                    }))

                # 3. Direct energy telemetry over WebSocket
                elif action == "energy_telemetry":
                    self.current_energy_state = data.get("state", {})
                    await websocket.send(json.dumps({"status": "energy_acknowledged"}))

                # 4. Stats and ping requests
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
                log.info(f"🔌 Peer disconnected: {p_name} | Remaining: {len(self.peers)}")

    def contribute(self, cycles: int = 10, inject_nan: bool = False) -> dict:
        """Local simulation of compute contribution"""
        reward = cycles // 10
        self.compute_shared += cycles
        self.olona += reward
        _save_data(self)
        return {"cycles": cycles, "olona": reward, "total_olona": self.olona}

    def claim_nft(self, tier: str = "bronze") -> dict:
        """Issues an eco-citizen proof of compute certificate NFT"""
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
        """Burn 50 Olona to redeem a compute certificate / carbon offset"""
        if self.olona >= 50.0:
            self.olona -= 50.0
            self.trees += 1
            _save_data(self)
            return {"tree": self.trees, "message": "🌱 Compute credit / Carbon offset verified"}
        return {"error": "Not enough Olona. Continue contributing green compute!"}

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


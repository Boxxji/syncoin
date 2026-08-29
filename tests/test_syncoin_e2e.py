#!/usr/bin/env python3
"""
SynCoin E2E Test Suite — MIT License
Tests the complete Decarbonized Compute Mesh pipeline:
Solar/Battery Energy Arbiter ➔ P2P Node ➔ Universal Workers ➔ Proof of Compute ➔ Olona Rewards
"""
from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from syncoin_node import SynCoinNode
from syncoin_energy_daemon import EnergyArbiter
from syncoin_worker import SynCoinWorker

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("TestSynCoinE2E")


class TestSynCoinDecarbonizedMesh(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.test_port = 18788
        self.node = SynCoinNode(
            node_id="test-master-hub",
            port=self.test_port,
            nats_url=None,  # Standalone WebSocket for test isolation
            data_file="test_syncoin_data.json"
        )
        self.arbiter = EnergyArbiter(
            min_surplus_threshold_watts=200.0,
            battery_min_soc_reserve=30.0,
            battery_green_compute_soc=80.0,
            nats_url=None
        )
        # Start node in background task
        self.node_task = asyncio.create_task(self.node.start())
        await asyncio.sleep(0.5)  # Wait for socket bind

    async def asyncTearDown(self):
        self.node_task.cancel()
        try:
            await self.node_task
        except asyncio.CancelledError:
            pass
        if os.path.exists("test_syncoin_data.json"):
            os.remove("test_syncoin_data.json")

    async def test_01_energy_arbiter_logic(self):
        """Vérifie les 4 états d'arbitrage Solaire et Batterie"""
        log.info("🧪 [TEST 1] Vérification de l'Arbitrage Énergétique...")

        # Cas 1 : Surplus solaire puissant (2500W solaire, 400W maison)
        s1 = self.arbiter.evaluate_energy(solar_w=2500.0, home_w=400.0, battery_soc=60.0)
        self.assertTrue(s1.compute_allowed)
        self.assertEqual(s1.energy_source_tag, "GREEN_SOLAR")
        self.assertEqual(s1.surplus_watts, 2100.0)

        # Cas 2 : Surplus batterie verte (100W solaire, 85% batterie)
        s2 = self.arbiter.evaluate_energy(solar_w=100.0, home_w=300.0, battery_soc=85.0)
        self.assertTrue(s2.compute_allowed)
        self.assertEqual(s2.energy_source_tag, "GREEN_BATTERY")

        # Cas 3 : Batterie sous le seuil de réserve vital (0W solaire, 25% batterie)
        s3 = self.arbiter.evaluate_energy(solar_w=0.0, home_w=400.0, battery_soc=25.0)
        self.assertFalse(s3.compute_allowed)
        self.assertEqual(s3.energy_source_tag, "BATTERY_RESERVE_HOLD")

        # Cas 4 : Nuit sans batterie suffisante (0W solaire, 50% batterie)
        s4 = self.arbiter.evaluate_energy(solar_w=0.0, home_w=400.0, battery_soc=50.0)
        self.assertFalse(s4.compute_allowed)
        self.assertEqual(s4.energy_source_tag, "PAUSED")

        log.info("✅ [TEST 1] Arbitrage Solaire & Batterie 100% Conforme !")

    async def test_02_e2e_worker_compute_and_rewards(self):
        """Vérifie le cycle complet de calcul : Worker -> Node -> Proof of Compute -> Olona"""
        log.info("🧪 [TEST 2] Cycle Complet Worker ➔ Preuve de Calcul ➔ Récompenses...")

        initial_olona = self.node.olona

        # Création et lancement d'un Worker universel
        worker = SynCoinWorker(
            server_uri=f"ws://127.0.0.1:{self.test_port}",
            worker_id="worker-green-mac-test",
            require_ac_power=False  # Permet l'exécution de test
        )
        worker_task = asyncio.create_task(worker.run())
        await asyncio.sleep(0.5)  # Attente de connexion et d'enregistrement

        # 1. Vérification que le pair est bien enregistré dans le Nœud
        self.assertEqual(len(self.node.peers), 1)
        peer_entry = list(self.node.peers.values())[0]
        self.assertEqual(peer_entry["node"], "worker-green-mac-test")
        log.info(f"🤝 Pair connecté et reconnu : {peer_entry['node']}")

        # 2. Envoi d'un micro-job WASM
        test_payload = base64.b64encode(b"WASM_MICRO_TASK_BIOACOUSTIC_SPECTROGRAM_001").decode()
        dispatched = await self.node.dispatch_job(payload=test_payload, job_id="job-e2e-001")
        self.assertTrue(dispatched)

        # Attente du calcul et du renvoi du résultat
        await asyncio.sleep(0.8)

        # 3. Vérification des résultats
        self.assertEqual(worker.total_jobs_completed, 1)
        self.assertGreater(worker.total_olona_earned, 0.0)
        self.assertEqual(self.node.compute_shared, 1)
        self.assertGreater(self.node.olona, initial_olona)
        log.info(f"🌱 Solde Olona après calcul : {self.node.olona:.2f} (+{self.node.olona - initial_olona:.2f})")

        # 4. Plantation d'arbre via ASBL (Burn d'Olona)
        self.node.olona = 120.0  # Assure solde suffisant pour le test
        tree_res = self.node.plant_tree()
        self.assertIn("tree", tree_res)
        self.assertEqual(self.node.trees, 1)
        self.assertEqual(self.node.olona, 70.0)
        log.info(f"🌳 Arbre planté avec succès ! Message: {tree_res['message']}")

        # Arrêt du worker
        worker.is_running = False
        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            pass

        log.info("✅ [TEST 2] Cycle End-to-End Validé à 100% !")


if __name__ == "__main__":
    unittest.main()

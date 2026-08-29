#!/usr/bin/env python3
"""
SynCoin Energy Arbiter Daemon v1.0 — MIT License
Universal Residential Micro-Neocloud & BESS Energy Manager
Monitors Solar Surplus & Battery State of Charge (SoC) to trigger green AI compute.
"""
from __future__ import annotations

import asyncio
import json
import logging
import math
import os
import sys
import time
from dataclasses import asdict, dataclass
from typing import Optional

try:
    import nats
except ImportError:
    nats = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [SynCoin-Energy] %(message)s"
)
log = logging.getLogger("SynCoinEnergy")


@dataclass
class EnergyState:
    timestamp: float
    solar_power_watts: float
    home_consumption_watts: float
    battery_soc_percent: float
    battery_power_watts: float  # >0 = charging, <0 = discharging
    grid_power_watts: float     # >0 = importing, <0 = exporting
    surplus_watts: float
    compute_allowed: bool
    compute_power_target_watts: float
    energy_source_tag: str      # GREEN_SOLAR, GREEN_BATTERY, GRID_OFFPEAK, PAUSED


class EnergyArbiter:
    def __init__(
        self,
        min_surplus_threshold_watts: float = 200.0,
        battery_min_soc_reserve: float = 30.0,
        battery_green_compute_soc: float = 80.0,
        nats_url: Optional[str] = "nats://localhost:4222",
        simulation_mode: bool = False
    ):
        self.min_surplus = min_surplus_threshold_watts
        self.min_soc_reserve = battery_min_soc_reserve
        self.green_soc = battery_green_compute_soc
        self.nats_url = nats_url
        self.simulation_mode = simulation_mode
        self.nc = None
        self.is_running = False

    async def connect_nats(self):
        if not self.nats_url or nats is None:
            log.warning("NATS not available or disabled — running in standalone event mode")
            return
        try:
            self.nc = await nats.connect(self.nats_url)
            log.info(f"📡 Connected to NATS broker for energy telemetry: {self.nats_url}")
        except Exception as e:
            log.warning(f"⚠️ NATS connection failed ({e}) — local telemetry only")
            self.nc = None

    def evaluate_energy(
        self,
        solar_w: float,
        home_w: float,
        battery_soc: float,
        battery_power_w: float = 0.0,
        grid_w: float = 0.0
    ) -> EnergyState:
        now = time.time()
        surplus = solar_w - home_w
        compute_allowed = False
        target_compute_w = 0.0
        tag = "PAUSED"

        # 1. Direct Solar Priority (Sufficient surplus)
        if surplus >= self.min_surplus:
            compute_allowed = True
            target_compute_w = surplus
            tag = "GREEN_SOLAR"
        # 2. Green Battery Arbitrage (Battery well charged > 80%)
        elif battery_soc >= self.green_soc and battery_soc > self.min_soc_reserve:
            compute_allowed = True
            target_compute_w = min(500.0, (battery_soc - self.min_soc_reserve) * 10)
            tag = "GREEN_BATTERY"
        # 3. Battery below emergency reserve (Home protection)
        elif battery_soc <= self.min_soc_reserve:
            compute_allowed = False
            target_compute_w = 0.0
            tag = "BATTERY_RESERVE_HOLD"
        else:
            compute_allowed = False
            target_compute_w = 0.0
            tag = "PAUSED"

        return EnergyState(
            timestamp=now,
            solar_power_watts=round(solar_w, 2),
            home_consumption_watts=round(home_w, 2),
            battery_soc_percent=round(battery_soc, 2),
            battery_power_watts=round(battery_power_w, 2),
            grid_power_watts=round(grid_w, 2),
            surplus_watts=round(surplus, 2),
            compute_allowed=compute_allowed,
            compute_power_target_watts=round(target_compute_w, 2),
            energy_source_tag=tag
        )

    async def publish_telemetry(self, state: EnergyState):
        log.info(
            f"⚡ [Telemetry] Solar: {state.solar_power_watts}W | "
            f"Home: {state.home_consumption_watts}W | Surplus: {state.surplus_watts}W | "
            f"Battery: {state.battery_soc_percent}% | Tag: {state.energy_source_tag} | "
            f"Compute: {'🟢 ALLOWED' if state.compute_allowed else '🔴 PAUSED'}"
        )
        if self.nc:
            try:
                payload = json.dumps(asdict(state)).encode("utf-8")
                await self.nc.publish("syncoin.telemetry.energy", payload)
            except Exception as e:
                log.error(f"Erreur d'émission NATS: {e}")

    async def run_simulation_loop(self, duration_seconds: int = 60, tick_interval: float = 2.0):
        """Simule une journée solaire accélérée pour les tests end-to-end"""
        log.info(f"🌞 Démarrage de la simulation solaire ({duration_seconds}s)...")
        start_time = time.time()
        self.is_running = True

        while self.is_running and (time.time() - start_time < duration_seconds):
            elapsed = time.time() - start_time
            progress = (elapsed / duration_seconds) * math.pi  # 0 to PI (Sunrise to Sunset)

            # Courbe de cloche solaire (0W -> 3500W Peak -> 0W)
            solar_w = max(0.0, math.sin(progress) * 3500.0)
            home_w = 400.0 + 150.0 * math.cos(progress * 2)  # 250W à 550W de bruit domestique
            
            # Évolution de la batterie (charge avec le surplus)
            if solar_w > home_w:
                battery_soc = min(100.0, 40.0 + (solar_w - home_w) * (elapsed / duration_seconds) * 0.05)
            else:
                battery_soc = max(20.0, 40.0 - (elapsed / duration_seconds) * 15.0)

            state = self.evaluate_energy(solar_w, home_w, battery_soc)
            await self.broadcast_state(state)
            await asyncio.sleep(tick_interval)

        log.info("🏁 Simulation solaire terminée.")


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="SynCoin Solar & Battery Energy Arbiter")
    parser.add_argument("--nats", default="nats://localhost:4222", help="NATS Server URL")
    parser.add_argument("--sim", action="store_true", help="Run in accelerated solar simulation mode")
    parser.add_argument("--duration", type=int, default=30, help="Simulation duration in seconds")
    args = parser.parse_args()

    arbiter = EnergyArbiter(nats_url=args.nats, simulation_mode=args.sim)
    await arbiter.connect_nats()

    if args.sim:
        await arbiter.run_simulation_loop(duration_seconds=args.duration)
    else:
        log.info("Mode live en attente de flux énergétique (Ctrl+C pour quitter)...")
        while True:
            # En mode live autonome par défaut, lit 1000W solaire simulé
            state = arbiter.evaluate_energy(solar_w=1200.0, home_w=350.0, battery_soc=85.0)
            await arbiter.broadcast_state(state)
            await asyncio.sleep(5.0)


if __name__ == "__main__":
    asyncio.run(main())

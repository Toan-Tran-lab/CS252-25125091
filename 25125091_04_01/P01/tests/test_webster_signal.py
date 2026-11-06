"""Unit tests for Webster Traffic Signal Delay Modeling (Module M3).

Author: Tran Duc Toan (25125091)
"""

import math
import unittest
from datetime import datetime

from smartroute.routing.adapters import load_integrations
from smartroute.routing.costs import ReferenceCost
from smartroute.routing.types import CostBreakdown, Vehicle
from smartroute.signals.webster import (
    DEFAULT_SIGNAL_BY_HIGHWAY,
    ICT,
    calculate_node_signal_delay,
    get_congestion_factor_for_time,
    signal_delay,
    signal_delay_v1,
    signal_delay_v2,
    signal_delay_v3,
)


class TestWebsterIterations(unittest.TestCase):
    """Test 3 iterations of Computational Thinking for Signal Delay."""

    def test_v1_baseline_constant_delay(self):
        """V1 assigns a flat delay heuristic."""
        self.assertEqual(signal_delay_v1(15.0), 15.0)
        self.assertEqual(signal_delay_v1(0.0), 0.0)
        with self.assertRaises(ValueError):
            signal_delay_v1(-5.0)
        with self.assertRaises(ValueError):
            signal_delay_v1(math.nan)

    def test_v2_probabilistic_webster_uniform(self):
        """V2 calculates uniform expected delay: E[wait] = R^2 / (2 * (R + G))."""
        # Primary corridor: R=90s, G=30s -> E[wait] = 8100 / 240 = 33.75s
        delay = signal_delay_v2(90.0, 30.0)
        self.assertAlmostEqual(delay, 33.75, places=4)

        # Secondary corridor: R=60s, G=40s -> E[wait] = 3600 / 200 = 18.0s
        delay_sec = signal_delay_v2(60.0, 40.0)
        self.assertAlmostEqual(delay_sec, 18.0, places=4)

        # Edge case: No red light (Green wave or flashing amber)
        self.assertEqual(signal_delay_v2(0.0, 30.0), 0.0)

    def test_v3_context_aware_dynamic_congestion(self):
        """V3 scales uniform delay with time-of-day / queue congestion factor."""
        # Baseline uniform: 33.75s
        # Peak rush multiplier 1.2 -> 33.75 * 1.2 = 40.5s
        delay_peak = signal_delay_v3(90.0, 30.0, congestion_factor=1.2)
        self.assertAlmostEqual(delay_peak, 40.5, places=4)

        # Evening rush multiplier 1.5 -> 33.75 * 1.5 = 50.625s
        delay_heavy = signal_delay_v3(90.0, 30.0, congestion_factor=1.5)
        self.assertAlmostEqual(delay_heavy, 50.625, places=4)

    def test_v3_with_explicit_saturation_degree(self):
        """V3 calculates CF dynamically from saturation degree X = volume / capacity."""
        # R=90, G=30, X=0.6 -> lambda = 30/120 = 0.25 -> CF = 1 / (1 - 0.25 * 0.6) = 1 / 0.85
        expected_cf = 1.0 / (1.0 - (30.0 / 120.0) * 0.6)
        expected_delay = 33.75 * expected_cf
        actual_delay = signal_delay_v3(90.0, 30.0, saturation_x=0.6)
        self.assertAlmostEqual(actual_delay, expected_delay, places=4)

        with self.assertRaises(ValueError):
            signal_delay_v3(90.0, 30.0, saturation_x=1.0)  # Complete gridlock


class TestDefensiveValidation(unittest.TestCase):
    """Verify input validation and robustness against bad telemetry."""

    def test_negative_or_zero_values(self):
        with self.assertRaises(ValueError):
            signal_delay(-1.0, 30.0)
        with self.assertRaises(ValueError):
            signal_delay(90.0, 0.0)
        with self.assertRaises(ValueError):
            signal_delay(90.0, -10.0)

    def test_invalid_congestion_factor(self):
        with self.assertRaises(ValueError):
            signal_delay(90.0, 30.0, congestion_factor=0.8)  # Must be >= 1.0

    def test_non_finite_inputs(self):
        with self.assertRaises(ValueError):
            signal_delay(math.nan, 30.0)
        with self.assertRaises(ValueError):
            signal_delay(90.0, math.inf)
        with self.assertRaises(ValueError):
            signal_delay(90.0, 30.0, math.nan)


class TestHighLevelNodeCalculations(unittest.TestCase):
    """Verify road hierarchy resolution and timestamp-based delays."""

    def test_road_class_defaults(self):
        delay_primary = calculate_node_signal_delay(highway="primary", congestion_factor=1.0)
        delay_secondary = calculate_node_signal_delay(highway="secondary", congestion_factor=1.0)
        delay_tertiary = calculate_node_signal_delay(highway="tertiary", congestion_factor=1.0)

        # Primary corridors (R=90, G=30 -> 33.75s) have higher delay than secondary (R=60, G=40 -> 18s)
        self.assertAlmostEqual(delay_primary, 33.75, places=3)
        self.assertAlmostEqual(delay_secondary, 18.0, places=3)
        self.assertAlmostEqual(delay_tertiary, (40.0**2) / (2.0 * 70.0), places=3)
        self.assertGreater(delay_primary, delay_secondary)
        self.assertGreater(delay_secondary, delay_tertiary)

    def test_time_of_day_peak_resolution(self):
        # 17:30 ICT (Evening peak)
        dt_peak = datetime(2026, 11, 2, 17, 30, tzinfo=ICT)
        cf_peak = get_congestion_factor_for_time(dt_peak.timestamp())
        self.assertGreaterEqual(cf_peak, 1.4)

        # 02:00 ICT (Midnight off-peak)
        dt_night = datetime(2026, 11, 2, 2, 0, tzinfo=ICT)
        cf_night = get_congestion_factor_for_time(dt_night.timestamp())
        self.assertEqual(cf_night, 1.0)


class TestIntegrationWithThaiBaoRouter(unittest.TestCase):
    """Verify seamless compatibility with Thai Bao's router and adapter loader."""

    def test_load_integrations_discovers_toan(self):
        integrations = load_integrations()
        self.assertIn("signal=toan", integrations.label)
        self.assertIsNotNone(integrations.signal)

        # Verify integration call returns Webster delay
        res = integrations.signal(90.0, 30.0, 1.2)
        self.assertAlmostEqual(res, 40.5, places=3)

    def test_reference_cost_executes_with_toan_signal(self):
        integrations = load_integrations()
        cost_model = ReferenceCost(model="V3", congestion_factor=1.0, integrations=integrations)

        edge_data = {
            "length": 100.0,
            "speed_base_mps": 10.0,
            "signal": True,
            "highway": "primary",
            "red_s": 90.0,
            "green_s": 30.0,
            "signal_cf": 1.2,
            "car_ok": True,
        }

        # edge traversal time: 100m / 10m/s = 10s (drive)
        # signal delay: 40.5s
        # total cost: 10 + 40.5 = 50.5s
        total_cost, breakdown = cost_model((1, 2, 0), edge_data, t_arrival=1700000000.0, vehicle=Vehicle.SEDAN)
        self.assertAlmostEqual(breakdown.drive_s, 10.0, places=3)
        self.assertAlmostEqual(breakdown.signal_s, 40.5, places=3)
        self.assertAlmostEqual(total_cost, 50.5, places=3)


if __name__ == "__main__":
    unittest.main()

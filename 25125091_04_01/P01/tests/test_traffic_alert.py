"""Unit tests for Proximity Hazard Alert System.

Author: Tran Duc Toan (25125091)
"""

import unittest

from smartroute.alerts.proximity import (
    AlertLevel,
    AlertModality,
    check_route_proximity_alerts,
    evaluate_edge_hazard,
    haversine_distance_m,
)
from smartroute.routing.stubs import DictOverlay
from smartroute.routing.types import HazardState, Vehicle


class TestHaversineDistance(unittest.TestCase):
    """Verify geodetic distance calculations."""

    def test_zero_distance_same_point(self):
        coord = (10.8012, 106.7115)
        self.assertAlmostEqual(haversine_distance_m(coord, coord), 0.0, places=3)

    def test_known_distance_binh_thanh(self):
        # Hang Xanh roundabout to Landmark 81 (~1.8 km)
        hang_xanh = (10.8015, 106.7115)
        landmark_81 = (10.7950, 106.7218)
        dist = haversine_distance_m(hang_xanh, landmark_81)
        self.assertGreater(dist, 1300.0)
        self.assertLess(dist, 2000.0)


class TestDeonticHazardEvaluation(unittest.TestCase):
    """Test vehicle-specific Deontic hazard rules and alert modalities."""

    def test_deontic_flood_tiers_across_vehicle_classes(self):
        # 30cm flood scenario on an edge 50m ahead
        hazard_30cm = HazardState(depth_m=0.30, flags=frozenset(["FLOOD"]), t_report=100.0)
        edge = (1, 2, 0)

        # 1. Automatic Scooter (H_safe = 20cm) -> CRITICAL (exceeds clearance by 10cm)
        alert_scooter = evaluate_edge_hazard(edge, hazard_30cm, Vehicle.SCOOTER_AUTO, distance_m=50.0)
        self.assertEqual(alert_scooter.level, AlertLevel.CRITICAL)
        self.assertTrue(alert_scooter.reroute_suggested)
        self.assertAlmostEqual(alert_scooter.clearance_margin_m, -0.10, places=3)
        self.assertIn(AlertModality.SOUND, alert_scooter.modalities)
        self.assertIn(AlertModality.VIBRATION, alert_scooter.modalities)
        self.assertIn(AlertModality.POPUP, alert_scooter.modalities)

        # 2. Sedan (H_safe = 25cm) -> CRITICAL (exceeds clearance by 5cm)
        alert_sedan = evaluate_edge_hazard(edge, hazard_30cm, Vehicle.SEDAN, distance_m=50.0)
        self.assertEqual(alert_sedan.level, AlertLevel.CRITICAL)
        self.assertTrue(alert_sedan.reroute_suggested)
        self.assertAlmostEqual(alert_sedan.clearance_margin_m, -0.05, places=3)

        # 3. Manual Motorbike (H_safe = 30cm) -> WARNING (exactly at threshold, passable with drag)
        alert_manual = evaluate_edge_hazard(edge, hazard_30cm, Vehicle.MOTORBIKE_MANUAL, distance_m=50.0)
        self.assertEqual(alert_manual.level, AlertLevel.WARNING)
        self.assertFalse(alert_manual.reroute_suggested)
        self.assertAlmostEqual(alert_manual.clearance_margin_m, 0.00, places=3)
        self.assertNotIn(AlertModality.VIBRATION, alert_manual.modalities)

        # 4. SUV (H_safe = 50cm) -> WARNING (20cm safety margin)
        alert_suv = evaluate_edge_hazard(edge, hazard_30cm, Vehicle.SUV, distance_m=50.0)
        self.assertEqual(alert_suv.level, AlertLevel.WARNING)
        self.assertFalse(alert_suv.reroute_suggested)
        self.assertAlmostEqual(alert_suv.clearance_margin_m, 0.20, places=3)

    def test_road_closure_overrides_vehicle_clearance(self):
        # A road barrier / barricade (CLOSED flag)
        barrier = HazardState(depth_m=0.0, flags=frozenset(["CLOSED"]), t_report=100.0)
        edge = (2, 3, 0)

        # SUV must still be stopped and rerouted
        alert_suv = evaluate_edge_hazard(edge, barrier, Vehicle.SUV, distance_m=30.0)
        self.assertEqual(alert_suv.level, AlertLevel.CRITICAL)
        self.assertEqual(alert_suv.hazard_type, "BLOCKED")
        self.assertTrue(alert_suv.reroute_suggested)

    def test_pothole_triggers_info_alert(self):
        pothole = HazardState(depth_m=0.0, flags=frozenset(["POTHOLE"]), t_report=100.0)
        edge = (3, 4, 0)

        alert = evaluate_edge_hazard(edge, pothole, Vehicle.SCOOTER_AUTO, distance_m=40.0)
        self.assertEqual(alert.level, AlertLevel.INFO)
        self.assertEqual(alert.modalities, (AlertModality.POPUP,))
        self.assertFalse(alert.reroute_suggested)
        self.assertIn("ổ gà", alert.message_vi)


class TestRouteLookaheadProximityScanning(unittest.TestCase):
    """Test full route scanning within look-ahead horizon."""

    def setUp(self):
        self.edges = [(0, 1, 0), (1, 2, 0), (2, 3, 0), (3, 4, 0)]
        self.edge_lengths = {
            (0, 1, 0): 30.0,
            (1, 2, 0): 40.0,
            (2, 3, 0): 50.0,
            (3, 4, 0): 60.0,
        }

    def test_clean_route_returns_no_trigger(self):
        overlay = DictOverlay({})
        alert = check_route_proximity_alerts(
            current_coord=(10.80, 106.71),
            upcoming_edges=self.edges,
            overlay=overlay,
            vehicle=Vehicle.SCOOTER_AUTO,
            current_time=200.0,
            edge_lengths_map=self.edge_lengths,
        )
        self.assertFalse(alert.triggered)
        self.assertIsNone(alert.level)

    def test_hazard_beyond_lookahead_is_ignored(self):
        # Hazard at edge (3, 4, 0) which is 30+40+50 = 120m away (> 100m lookahead)
        overlay = DictOverlay({(3, 4, 0): HazardState(depth_m=0.40, flags=frozenset(["FLOOD"]), t_report=100.0)})
        alert = check_route_proximity_alerts(
            current_coord=(10.80, 106.71),
            upcoming_edges=self.edges,
            overlay=overlay,
            vehicle=Vehicle.SCOOTER_AUTO,
            current_time=200.0,
            edge_lengths_map=self.edge_lengths,
            lookahead_distance_m=100.0,
        )
        self.assertFalse(alert.triggered)

    def test_hazard_within_lookahead_triggers(self):
        # Hazard at edge (1, 2, 0) which is 30 + 20 = 50m away (< 100m lookahead)
        overlay = DictOverlay({(1, 2, 0): HazardState(depth_m=0.35, flags=frozenset(["FLOOD"]), t_report=100.0)})
        alert = check_route_proximity_alerts(
            current_coord=(10.80, 106.71),
            upcoming_edges=self.edges,
            overlay=overlay,
            vehicle=Vehicle.SCOOTER_AUTO,
            current_time=200.0,
            edge_lengths_map=self.edge_lengths,
            lookahead_distance_m=100.0,
        )
        self.assertTrue(alert.triggered)
        self.assertEqual(alert.level, AlertLevel.CRITICAL)
        self.assertEqual(alert.edge_id, (1, 2, 0))

    def test_priority_resolution_critical_wins_over_info(self):
        # Pothole at edge (0, 1, 0) [~15m away]
        # Critical flood at edge (1, 2, 0) [~50m away]
        overlay = DictOverlay({
            (0, 1, 0): HazardState(depth_m=0.0, flags=frozenset(["POTHOLE"]), t_report=100.0),
            (1, 2, 0): HazardState(depth_m=0.40, flags=frozenset(["FLOOD"]), t_report=100.0),
        })

        alert = check_route_proximity_alerts(
            current_coord=(10.80, 106.71),
            upcoming_edges=self.edges,
            overlay=overlay,
            vehicle=Vehicle.SCOOTER_AUTO,
            current_time=200.0,
            edge_lengths_map=self.edge_lengths,
            lookahead_distance_m=100.0,
        )
        # CRITICAL takes priority over INFO even though INFO is closer
        self.assertEqual(alert.level, AlertLevel.CRITICAL)
        self.assertEqual(alert.edge_id, (1, 2, 0))


if __name__ == "__main__":
    unittest.main()

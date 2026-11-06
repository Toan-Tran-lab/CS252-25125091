"""Live Feature Demonstration: SmartRoute Traffic Signal Delay & Proximity Hazard Alerts.

Owner: Tran Duc Toan (25125091) - Group 06 - CS252 Computational Thinking
Demonstrates 'Feature in Action' for Lab 04 Submission.
"""

import sys
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# Add local src and sibling group repo src to sys.path
src_path = Path(__file__).resolve().parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

sibling_group_src = Path(__file__).resolve().parents[3] / "CS252-Group6" / "src"
if sibling_group_src.exists() and str(sibling_group_src) not in sys.path:
    sys.path.insert(0, str(sibling_group_src))

from smartroute.signals.webster import (
    signal_delay_v1,
    signal_delay_v2,
    signal_delay_v3,
    get_congestion_factor_for_time,
    signal_delay,
)
from smartroute.alerts.proximity import (
    AlertLevel,
    check_route_proximity_alerts,
    evaluate_edge_hazard,
)
from smartroute.routing.types import EdgeId, HazardState, Vehicle


def print_banner(title: str):
    width = 75
    print("\n" + "=" * width)
    print(f" {title.center(width - 2)} ")
    print("=" * width)


def demo_webster_signal_delay():
    print_banner("DEMO 1: TRAFFIC SIGNAL DELAY MODELING (WEBSTER V1 -> V2 -> V3)")

    red_s = 90.0
    green_s = 30.0
    cycle_s = red_s + green_s

    print(f"Intersection: Dien Bien Phu x D1 (Binh Thanh District)")
    print(f"Timing Configuration: Red = {red_s:.1f}s | Green = {green_s:.1f}s | Cycle = {cycle_s:.1f}s\n")

    # V1: Baseline Heuristic
    d_v1 = signal_delay_v1()
    print(f"[*] Iteration 1 (V1 Baseline):")
    print(f"    - Formula: Flat heuristic delay = 15.0s")
    print(f"    => Expected Delay E[d]: {d_v1:.2f} seconds\n")

    # V2: Probabilistic Webster
    d_v2 = signal_delay_v2(red_s, green_s)
    print(f"[*] Iteration 2 (V2 Probabilistic Webster - Uniform Arrival):")
    print(f"    - Formula: E[wait] = R^2 / (2 * (R + G))")
    print(f"    - E[wait] = {red_s}^2 / (2 * {cycle_s}) = {red_s**2:.0f} / {2*cycle_s:.0f}")
    print(f"    => Expected Delay E[d]: {d_v2:.2f} seconds\n")

    # V3: Context-Aware Dynamic
    print(f"[*] Iteration 3 (V3 Context-Aware Dynamic with Time-of-Day):")
    base_midnight = 1793811600.0  # arbitrary reference day
    hours_to_test = [
        (2.0, "Midnight (Low Traffic)"),
        (8.0, "Morning Rush Hour (Heavy Congestion)"),
        (14.0, "Afternoon Normal (Moderate Traffic)"),
        (17.5, "Evening Rush Hour (Peak Saturation)"),
    ]

    for hour, label in hours_to_test:
        ts = base_midnight + hour * 3600.0
        cf = get_congestion_factor_for_time(ts)
        d_v3 = signal_delay_v3(red_s, green_s, congestion_factor=cf)
        delta_pct = ((d_v3 - d_v2) / d_v2) * 100.0
        print(f"    - Time {hour:04.1f}h ({label}):")
        print(f"      Congestion Factor = {cf:.2f}x | Delay E[d] = {d_v3:.2f}s ({delta_pct:+.1f}% vs V2)")


def demo_proximity_hazard_alerts():
    print_banner("DEMO 2: REAL-TIME PROXIMITY HAZARD WARNING SYSTEM (DEONTIC TIERS)")

    current_coord = (10.8015, 106.7110)  # Near Ung Van Khiem & D2
    print(f"Commuter GPS Position: {current_coord} (Binh Thanh)")
    print(f"Current Speed: 30.0 km/h (8.33 m/s) | Lookahead Horizon: 100 metres\n")

    test_edge: EdgeId = (1001, 1002, 0)
    hazard_coord = (10.8019, 106.7114)  # ~65 metres ahead

    # Scenario A: Deep Flood (30cm) evaluated for different vehicles
    print("-" * 75)
    print("SCENARIO A: ROAD FLOOD DEPTH = 30 cm (~65m ahead)")
    print("-" * 75)

    flood_hazard = HazardState(depth_m=0.30, flags=frozenset(), t_report=0.0)

    for vehicle in [Vehicle.SCOOTER_AUTO, Vehicle.SEDAN, Vehicle.MOTORBIKE_MANUAL, Vehicle.SUV]:
        payload = evaluate_edge_hazard(
            edge=test_edge,
            hazard_state=flood_hazard,
            vehicle=vehicle,
            distance_m=65.0,
            speed_mps=8.33,
            hazard_coord=hazard_coord,
        )
        status_tag = f"[{payload.level.value}]" if payload.level else "[SAFE]"
        modalities_str = ", ".join(m.value.upper() for m in payload.modalities)
        margin_str = f"{payload.clearance_margin_m * 100:+.1f}cm" if payload.clearance_margin_m is not None else "N/A"
        print(f"\n>> Vehicle: {vehicle.name:18} (Ground Clearance H_safe = {vehicle.h_safe * 100:.0f}cm)")
        print(f"   Alert Level  : {status_tag}")
        print(f"   Modalities   : {modalities_str}")
        print(f"   Clearance    : {margin_str} margin")
        print(f"   Message (VI) : {payload.message_vi}")
        print(f"   Reroute Req. : {'YES (Trigger Failover Routing)' if payload.reroute_suggested else 'NO (Safe to pass with caution)'}")

    # Scenario B: Road Closed / Construction
    print("\n" + "-" * 75)
    print("SCENARIO B: ROAD CLOSURE & ROAD DEFECTS")
    print("-" * 75)

    closure_hazard = HazardState(depth_m=0.0, flags=frozenset(["CLOSED"]), t_report=0.0)
    payload_closed = evaluate_edge_hazard(
        edge=test_edge,
        hazard_state=closure_hazard,
        vehicle=Vehicle.SUV,
        distance_m=50.0,
        speed_mps=8.33,
        hazard_coord=hazard_coord,
    )
    print(f"\n>> Case 1: Road Closed Ahead (Distance 50m)")
    print(f"   Alert Level  : [{payload_closed.level.value}]")
    print(f"   Modalities   : {', '.join(m.value.upper() for m in payload_closed.modalities)}")
    print(f"   Message (VI) : {payload_closed.message_vi}")
    print(f"   Reroute Req. : {payload_closed.reroute_suggested}")

    pothole_hazard = HazardState(depth_m=0.02, flags=frozenset(["POTHOLE"]), t_report=0.0)
    payload_pothole = evaluate_edge_hazard(
        edge=test_edge,
        hazard_state=pothole_hazard,
        vehicle=Vehicle.SCOOTER_AUTO,
        distance_m=40.0,
        speed_mps=8.33,
        hazard_coord=hazard_coord,
    )
    print(f"\n>> Case 2: Deep Pothole Reported Ahead (Distance 40m)")
    print(f"   Alert Level  : [{payload_pothole.level.value}]")
    print(f"   Modalities   : {', '.join(m.value.upper() for m in payload_pothole.modalities)}")
    print(f"   Message (VI) : {payload_pothole.message_vi}")
    print(f"   Reroute Req. : {payload_pothole.reroute_suggested}")

    # Scenario C: Route Lookahead Scanning
    print("\n" + "-" * 75)
    print("SCENARIO C: REAL-TIME LOOKAHEAD ROUTE SCANNING")
    print("-" * 75)
    route_edges = [(1, 2, 0), (2, 3, 0), (3, 4, 0), (4, 5, 0)]
    overlay_map = {
        (2, 3, 0): HazardState(depth_m=0.25, flags=frozenset(), t_report=0.0),
    }
    coords_map = {
        (1, 2, 0): (10.8015, 106.7110),
        (2, 3, 0): (10.8019, 106.7115),  # ~70m ahead
        (3, 4, 0): (10.8028, 106.7125),  # ~180m ahead (outside 100m lookahead)
        (4, 5, 0): (10.8035, 106.7135),
    }

    scan_result = check_route_proximity_alerts(
        current_coord=(10.8015, 106.7110),
        upcoming_edges=route_edges,
        overlay=overlay_map,
        vehicle=Vehicle.SCOOTER_AUTO,
        current_time=0.0,
        edge_coords_map=coords_map,
        lookahead_distance_m=100.0,
    )
    print(f"Upcoming Edges : {len(route_edges)} segments")
    print(f"Lookahead Scan : Detected hazard at edge {scan_result.edge_id} within 100m horizon!")
    print(f"Trigger Status : Triggered={scan_result.triggered} | Level=[{scan_result.level.value}] | Time to Hazard={scan_result.time_to_hazard_s:.1f}s")
    print(f"Message (VI)   : {scan_result.message_vi}")
    print_banner("DEMONSTRATION COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    demo_webster_signal_delay()
    demo_proximity_hazard_alerts()

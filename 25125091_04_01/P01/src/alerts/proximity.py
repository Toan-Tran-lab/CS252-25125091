"""Proximity Hazard Alert and Multi-Modal Notification Trigger System.

Monitors real-time commuter proximity to road obstacles, floods, and closures,
evaluating Deontic safety constraints against vehicle clearance thresholds (H_safe).

Report reference: Section 4.3 (Flooding & Clearance Dynamics), Section 2.2.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

from smartroute.routing.types import EdgeId, HazardOverlay, HazardState, Vehicle


class AlertLevel(str, Enum):
    """Categorized hazard severity levels."""

    INFO = "INFO"           # Minor road defects (pothole, construction, puddles < 5cm)
    WARNING = "WARNING"     # Manageable flood (5cm <= depth <= H_safe), reduced speed
    CRITICAL = "CRITICAL"   # Unpassable barrier (depth > H_safe or CLOSED), reroute needed


class AlertModality(str, Enum):
    """UI notification output channels."""

    POPUP = "popup"
    SOUND = "sound"
    VIBRATION = "vibration"


@dataclass(frozen=True)
class AlertPayload:
    """Standardized alert payload delivered to frontend UI and voice assistants."""

    triggered: bool
    level: AlertLevel | None
    hazard_type: str | None
    distance_m: float
    time_to_hazard_s: float
    water_depth_m: float
    clearance_margin_m: float | None
    modalities: tuple[AlertModality, ...]
    message_vi: str
    reroute_suggested: bool
    edge_id: EdgeId | None = None
    hazard_coord: tuple[float, float] | None = None


def haversine_distance_m(
    coord1: tuple[float, float], coord2: tuple[float, float]
) -> float:
    """Calculate the great-circle distance between two (lat, lon) points in metres."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    r = 6371000.0  # Earth radius in metres

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c


def evaluate_edge_hazard(
    edge: EdgeId,
    hazard_state: HazardState,
    vehicle: Vehicle,
    distance_m: float,
    speed_mps: float = 8.33,
    hazard_coord: tuple[float, float] | None = None,
) -> AlertPayload:
    """Evaluate Deontic rules and generate an AlertPayload for an edge."""
    speed = max(speed_mps, 1.0)
    time_to_hazard = distance_m / speed
    depth = hazard_state.depth_m if math.isfinite(hazard_state.depth_m) else 0.0
    flags = hazard_state.flags

    # Case 1: Road explicitly closed / blocked
    if "CLOSED" in flags:
        return AlertPayload(
            triggered=True,
            level=AlertLevel.CRITICAL,
            hazard_type="BLOCKED",
            distance_m=distance_m,
            time_to_hazard_s=time_to_hazard,
            water_depth_m=depth,
            clearance_margin_m=None,
            modalities=(AlertModality.POPUP, AlertModality.SOUND, AlertModality.VIBRATION),
            message_vi=f"NGUY HIỂM: Phía trước {distance_m:.0f}m đường bị chặn hoàn toàn! Vui lòng chuyển hướng!",
            reroute_suggested=True,
            edge_id=edge,
            hazard_coord=hazard_coord,
        )

    # Case 2: Water depth exceeds vehicle clearance threshold (H_safe)
    if depth > vehicle.h_safe:
        deficit = depth - vehicle.h_safe
        return AlertPayload(
            triggered=True,
            level=AlertLevel.CRITICAL,
            hazard_type="FLOOD_CRITICAL",
            distance_m=distance_m,
            time_to_hazard_s=time_to_hazard,
            water_depth_m=depth,
            clearance_margin_m=-deficit,
            modalities=(AlertModality.POPUP, AlertModality.SOUND, AlertModality.VIBRATION),
            message_vi=(
                f"NGUY HIỂM: Phía trước {distance_m:.0f}m ngập sâu {depth * 100:.0f}cm "
                f"(vượt gầm xe {deficit * 100:.0f}cm)! Dừng xe hoặc chuyển hướng ngay!"
            ),
            reroute_suggested=True,
            edge_id=edge,
            hazard_coord=hazard_coord,
        )

    # Case 3: Water depth is passable with caution (0.05m <= depth <= H_safe)
    if depth >= 0.05:
        margin = vehicle.h_safe - depth
        return AlertPayload(
            triggered=True,
            level=AlertLevel.WARNING,
            hazard_type="FLOOD_PASSABLE",
            distance_m=distance_m,
            time_to_hazard_s=time_to_hazard,
            water_depth_m=depth,
            clearance_margin_m=margin,
            modalities=(AlertModality.POPUP, AlertModality.SOUND),
            message_vi=(
                f"CHÚ Ý: Phía trước {distance_m:.0f}m ngập {depth * 100:.0f}cm. "
                f"Gầm xe còn an toàn ({margin * 100:.0f}cm), hãy giảm tốc độ."
            ),
            reroute_suggested=False,
            edge_id=edge,
            hazard_coord=hazard_coord,
        )

    # Case 4: Physical road defects (pothole, construction, minor puddle)
    defect_label = "ổ gà / mặt đường xấu"
    if "POTHOLE" in flags:
        defect_label = "ổ gà sâu"
    elif "CONSTRUCTION" in flags:
        defect_label = "công trình rào chắn"

    return AlertPayload(
        triggered=True,
        level=AlertLevel.INFO,
        hazard_type="ROAD_DEFECT",
        distance_m=distance_m,
        time_to_hazard_s=time_to_hazard,
        water_depth_m=depth,
        clearance_margin_m=vehicle.h_safe,
        modalities=(AlertModality.POPUP,),
        message_vi=f"THÔNG BÁO: Phía trước {distance_m:.0f}m có {defect_label}. Vui lòng chú ý quan sát.",
        reroute_suggested=False,
        edge_id=edge,
        hazard_coord=hazard_coord,
    )


def check_route_proximity_alerts(
    current_coord: tuple[float, float],
    upcoming_edges: Sequence[EdgeId],
    overlay: HazardOverlay | Mapping[EdgeId, HazardState],
    vehicle: Vehicle,
    current_time: float,
    edge_coords_map: Mapping[EdgeId, tuple[float, float]] | None = None,
    edge_lengths_map: Mapping[EdgeId, float] | None = None,
    current_speed_mps: float = 8.33,
    lookahead_distance_m: float = 100.0,
) -> AlertPayload:
    """Scan upcoming route edges within look-ahead horizon and trigger highest-priority alert.
    
    Priority order: CRITICAL > WARNING > INFO. Within same level, closer distance wins.
    """
    severity_order = {AlertLevel.CRITICAL: 3, AlertLevel.WARNING: 2, AlertLevel.INFO: 1}
    best_alert: AlertPayload | None = None
    accumulated_distance = 0.0

    for edge in upcoming_edges:
        edge_len = 30.0
        if edge_lengths_map and edge in edge_lengths_map:
            edge_len = edge_lengths_map[edge]

        edge_coord = edge_coords_map.get(edge) if edge_coords_map else None

        # Distance estimation: direct geodetic if coord known, else accumulated segment lengths
        if edge_coord is not None:
            dist = haversine_distance_m(current_coord, edge_coord)
        else:
            dist = accumulated_distance + (edge_len / 2.0)

        accumulated_distance += edge_len

        # Stop evaluating if beyond look-ahead horizon
        if dist > lookahead_distance_m:
            break

        # Check hazard state
        if isinstance(overlay, dict):
            state = overlay.get(edge)
        elif hasattr(overlay, "get"):
            try:
                state = overlay.get(edge, current_time)
            except TypeError:
                state = overlay.get(edge)
        else:
            state = None

        if state is None:
            continue

        # Ignore clean roads with zero water and no flags
        if state.depth_m < 0.05 and not state.flags:
            continue

        alert = evaluate_edge_hazard(
            edge=edge,
            hazard_state=state,
            vehicle=vehicle,
            distance_m=dist,
            speed_mps=current_speed_mps,
            hazard_coord=edge_coord,
        )

        if best_alert is None:
            best_alert = alert
        else:
            cur_prio = severity_order.get(alert.level, 0)
            best_prio = severity_order.get(best_alert.level, 0)
            if cur_prio > best_prio:
                best_alert = alert
            elif cur_prio == best_prio and alert.distance_m < best_alert.distance_m:
                best_alert = alert

    if best_alert is not None:
        return best_alert

    # No hazard within lookahead range
    return AlertPayload(
        triggered=False,
        level=None,
        hazard_type=None,
        distance_m=math.inf,
        time_to_hazard_s=math.inf,
        water_depth_m=0.0,
        clearance_margin_m=vehicle.h_safe,
        modalities=(),
        message_vi="Lộ trình an toàn, không có chướng ngại vật phía trước.",
        reroute_suggested=False,
    )

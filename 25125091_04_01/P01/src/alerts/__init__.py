"""Traffic alert and proximity warning module for SmartRoute."""

from .proximity import (
    AlertLevel,
    AlertModality,
    AlertPayload,
    check_route_proximity_alerts,
    evaluate_edge_hazard,
    haversine_distance_m,
)

__all__ = [
    "AlertLevel",
    "AlertModality",
    "AlertPayload",
    "check_route_proximity_alerts",
    "evaluate_edge_hazard",
    "haversine_distance_m",
]

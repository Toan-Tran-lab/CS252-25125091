"""Traffic alert and proximity warning module for SmartRoute."""

from .proximity import (
    AlertLevel,
    AlertModality,
    AlertPayload,
    check_route_proximity_alerts,
    evaluate_edge_hazard,
    haversine_distance_m,
)
from .voice import (
    POTHOLE_VOICE_ALERT_VI,
    generate_web_speech_script,
    get_pothole_voice_text,
)

__all__ = [
    "AlertLevel",
    "AlertModality",
    "AlertPayload",
    "check_route_proximity_alerts",
    "evaluate_edge_hazard",
    "haversine_distance_m",
    "POTHOLE_VOICE_ALERT_VI",
    "generate_web_speech_script",
    "get_pothole_voice_text",
]

"""Traffic signals module for SmartRoute (Module M3)."""

from .webster import (
    DEFAULT_SIGNAL_BY_HIGHWAY,
    MEGA_INTERSECTIONS_WHITELIST,
    calculate_node_signal_delay,
    get_congestion_factor_for_time,
    signal_delay,
    signal_delay_v1,
    signal_delay_v2,
    signal_delay_v3,
)

__all__ = [
    "DEFAULT_SIGNAL_BY_HIGHWAY",
    "MEGA_INTERSECTIONS_WHITELIST",
    "calculate_node_signal_delay",
    "get_congestion_factor_for_time",
    "signal_delay",
    "signal_delay_v1",
    "signal_delay_v2",
    "signal_delay_v3",
]

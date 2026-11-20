"""Traffic signals module for SmartRoute (Module M3)."""

from .webster import (
    DEFAULT_SIGNAL_BY_HIGHWAY,
    MAJOR_INTERSECTIONS_WEBSTER_LOOKUP,
    MEGA_INTERSECTIONS_WHITELIST,
    calculate_node_signal_delay,
    format_eta_breakdown,
    get_all_major_intersections,
    get_congestion_factor_for_time,
    get_major_intersection_delay,
    signal_delay,
    signal_delay_v1,
    signal_delay_v2,
    signal_delay_v3,
)

__all__ = [
    "DEFAULT_SIGNAL_BY_HIGHWAY",
    "MAJOR_INTERSECTIONS_WEBSTER_LOOKUP",
    "MEGA_INTERSECTIONS_WHITELIST",
    "calculate_node_signal_delay",
    "format_eta_breakdown",
    "get_all_major_intersections",
    "get_congestion_factor_for_time",
    "get_major_intersection_delay",
    "signal_delay",
    "signal_delay_v1",
    "signal_delay_v2",
    "signal_delay_v3",
]

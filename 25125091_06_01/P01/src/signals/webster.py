"""Webster Traffic Signal Delay Modeling (Module M3).

This module implements the probabilistic intersection delay model based on
Webster's formula (1958) and its context-aware refinements across 3 CT iterations.

Report reference: Section 4.1 (Traffic Signal Delay Modeling), Eq. (4)
dsignal(v, t0) = R_v^2 / (2 * (R_v + G_v)) * CongestionFactor(t0)
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Any

ICT = timezone(timedelta(hours=7))

# Default signal cycle parameters (seconds) by road hierarchy in Binh Thanh
DEFAULT_SIGNAL_BY_HIGHWAY: dict[str, dict[str, float]] = {
    "primary": {"red_s": 90.0, "green_s": 30.0},
    "secondary": {"red_s": 60.0, "green_s": 40.0},
    "tertiary": {"red_s": 40.0, "green_s": 30.0},
    "default": {"red_s": 45.0, "green_s": 35.0},
}

# Hourly congestion multipliers for HCMC urban transit (0-23h ICT)
# Peak hours (07:00-08:59 and 17:00-18:59) experience queue backlogs across multiple cycles.
CONGESTION_BY_HOUR: list[float] = [
    1.00, 1.00, 1.00, 1.00, 1.00, 1.00,  # 00:00 - 05:59 (late night/early morning)
    1.10, 1.35, 1.40, 1.15, 1.10, 1.15,  # 06:00 - 11:59 (morning rush & midday)
    1.15, 1.10, 1.10, 1.15, 1.25, 1.50,  # 12:00 - 17:59 (afternoon & evening rush peak)
    1.45, 1.25, 1.10, 1.05, 1.00, 1.00,  # 18:00 - 23:59 (evening ramp down)
]

# Mega-intersections in Binh Thanh with automated long cycles
# (Prepared for future Track S-A deterministic override hook)
MEGA_INTERSECTIONS_WHITELIST: set[str] = {
    "hang_xanh",
    "pham_van_dong_phan_van_tri",
    "bach_dang_dinh_bo_linh",
    "dien_bien_phu_xo_viet_nghe_tinh",
}


def signal_delay_v1(base_delay: float = 15.0) -> float:
    """Iteration 1 (V1 Baseline): Constant delay heuristic.
    
    Assigns a fixed constant wait time to all signalized intersections regardless
    of phase timing, volume, or time of day.
    """
    if not math.isfinite(base_delay) or base_delay < 0:
        raise ValueError("Base delay must be a non-negative finite number")
    return float(base_delay)


def signal_delay_v2(red_s: float, green_s: float) -> float:
    """Iteration 2 (V2 Probabilistic): Uniform-arrival Webster delay.
    
    Assumes vehicle arrival times are distributed uniformly at random over
    the cycle length C = R + G.
    - Probability of arriving on red: P(Red) = R / (R + G)
    - Expected wait time given arrival on red: E[Wait | Red] = R / 2
    - Expected delay: E[Wait] = P(Red) * E[Wait | Red] = R^2 / (2 * (R + G))
    """
    _validate_signal_inputs(red_s, green_s, 1.0)
    if red_s == 0.0:
        return 0.0
    return (red_s * red_s) / (2.0 * (red_s + green_s))


def signal_delay_v3(
    red_s: float,
    green_s: float,
    congestion_factor: float = 1.0,
    *,
    saturation_x: float | None = None,
) -> float:
    """Iteration 3 (V3 Context-Aware Dynamic): Webster delay with congestion/queue clearance.
    
    Incorporates congestion factor CF >= 1.0, modeling queue overflow and clearance delay
    when traffic volume approaches or exceeds capacity.
    
    If saturation degree X is explicitly provided (0 <= X < 1):
        CF = 1.0 / (1.0 - (green_s / (red_s + green_s)) * X)
    """
    if saturation_x is not None:
        if not (0.0 <= saturation_x < 1.0):
            raise ValueError("Saturation degree X must be in [0, 1)")
        lambda_ratio = green_s / (red_s + green_s)
        congestion_factor = 1.0 / (1.0 - lambda_ratio * saturation_x)

    _validate_signal_inputs(red_s, green_s, congestion_factor)
    if red_s == 0.0:
        return 0.0

    uniform_delay = (red_s * red_s) / (2.0 * (red_s + green_s))
    return uniform_delay * congestion_factor


def get_congestion_factor_for_time(timestamp: float) -> float:
    """Resolve time-of-day congestion factor from epoch timestamp in ICT."""
    dt = datetime.fromtimestamp(timestamp, ICT)
    return CONGESTION_BY_HOUR[dt.hour]


def signal_delay(red_s: float, green_s: float, congestion_factor: float = 1.0) -> float:
    """Standard adapter interface matching smartroute.routing.adapters.Integrations.
    
    This matches the signature expected by Thai Bao's router and Tien Dung's W_eff.
    """
    return signal_delay_v3(red_s, green_s, congestion_factor)


def calculate_node_signal_delay(
    highway: str | list[str] = "default",
    timestamp: float | None = None,
    congestion_factor: float | None = None,
    custom_red_s: float | None = None,
    custom_green_s: float | None = None,
) -> float:
    """High-level junction delay calculator resolving road classes and timestamps."""
    if isinstance(highway, list):
        highway = sorted(highway)[0] if highway else "default"

    specs = DEFAULT_SIGNAL_BY_HIGHWAY.get(highway, DEFAULT_SIGNAL_BY_HIGHWAY["default"])
    r = custom_red_s if custom_red_s is not None else specs["red_s"]
    g = custom_green_s if custom_green_s is not None else specs["green_s"]

    if congestion_factor is None:
        if timestamp is not None:
            cf = get_congestion_factor_for_time(timestamp)
        else:
            cf = 1.0
    else:
        cf = congestion_factor

    return signal_delay(r, g, cf)


def _validate_signal_inputs(red_s: float, green_s: float, cf: float) -> None:
    if not (math.isfinite(red_s) and math.isfinite(green_s) and math.isfinite(cf)):
        raise ValueError("Signal timings and congestion factor must be finite numbers")
    if red_s < 0.0:
        raise ValueError(f"Red duration cannot be negative: {red_s}")
    if green_s <= 0.0:
        raise ValueError(f"Green duration must be strictly positive: {green_s}")
    if red_s + green_s <= 0.0:
        raise ValueError("Total cycle duration must be strictly positive")
    if cf < 1.0:
        raise ValueError(f"Congestion factor cannot be less than 1.0: {cf}")


# ==============================================================================
# MAJOR INTERSECTIONS WEBSTER DELAY LOOKUP TABLE (WEEK 08 TASK)
# ==============================================================================

MAJOR_INTERSECTIONS_WEBSTER_LOOKUP: dict[str, dict[str, Any]] = {
    "hang_xanh": {
        "id": "hang_xanh",
        "name": "Ngã tư Hàng Xanh",
        "delay_s": 45.0,
        "cycle_s": 120.0,
        "red_s": 90.0,
        "green_s": 30.0,
        "corridor": "Điện Biên Phủ – Xô Viết Nghệ Tĩnh",
        "aliases": ["hang_xanh", "hàng xanh", "ngã tư hàng xanh", "hang xanh"],
    },
    "d2_d5": {
        "id": "d2_d5",
        "name": "Giao lộ D2 – D5",
        "delay_s": 30.0,
        "cycle_s": 100.0,
        "red_s": 60.0,
        "green_s": 40.0,
        "corridor": "Nguyễn Gia Trí (D2) – D5",
        "aliases": ["d2_d5", "d2-d5", "d2 d5", "d2", "d5", "giao lộ d2 – d5", "nguyễn gia trí"],
    },
    "dinh_bo_linh": {
        "id": "dinh_bo_linh",
        "name": "Nút giao Đinh Bộ Lĩnh",
        "delay_s": 40.0,
        "cycle_s": 115.0,
        "red_s": 80.0,
        "green_s": 35.0,
        "corridor": "Đinh Bộ Lĩnh – Bạch Đằng",
        "aliases": ["dinh_bo_linh", "đinh bộ lĩnh", "dinh bo linh", "bạch đằng", "đinh bộ lĩnh – bạch đằng"],
    },
}


def get_major_intersection_delay(name: str) -> float:
    """Retrieve Webster expected delay in seconds for major Binh Thanh intersections."""
    raw = name.strip().lower()
    clean = raw.replace(" ", "_").replace("-", "_").replace("–", "_")
    for k, data in MAJOR_INTERSECTIONS_WEBSTER_LOOKUP.items():
        if k == clean or k in clean or clean in k:
            return float(data["delay_s"])
        for alias in data.get("aliases", []):
            alias_clean = alias.lower().replace(" ", "_").replace("-", "_").replace("–", "_")
            if alias_clean in clean or clean in alias_clean or alias in raw:
                return float(data["delay_s"])
    raise KeyError(f"Unknown intersection in lookup table: {name}")


def get_all_major_intersections() -> dict[str, dict[str, Any]]:
    """Return the full lookup table of major intersection delays."""
    return dict(MAJOR_INTERSECTIONS_WEBSTER_LOOKUP)


def format_eta_breakdown(
    driving_time_s: float, intersections: list[str]
) -> dict[str, Any]:
    """Decompose total ETA into driving duration + Webster intersection signal delays.
    
    Fulfills Widget 3: ETA = Lăn bánh + Chờ đèn (Webster).
    """
    signal_delays = [
        (name, get_major_intersection_delay(name)) for name in intersections
    ]
    total_signal_s = sum(delay for _, delay in signal_delays)
    total_eta_s = driving_time_s + total_signal_s
    driving_mins = max(1, round(driving_time_s / 60.0))
    total_eta_mins = max(1, round(total_eta_s / 60.0))

    intersection_labels = []
    for item in intersections:
        matched = False
        raw = item.strip().lower()
        clean = raw.replace(" ", "_").replace("-", "_").replace("–", "_")
        for k, data in MAJOR_INTERSECTIONS_WEBSTER_LOOKUP.items():
            if k == clean or k in clean or any(a in raw for a in data.get("aliases", [])):
                intersection_labels.append(data["name"])
                matched = True
                break
        if not matched:
            intersection_labels.append(item)

    names_str = ", ".join(intersection_labels) if intersection_labels else "Không có"
    breakdown_text = f"ETA = {driving_mins} phút lăn bánh + {int(total_signal_s)}s chờ đèn (Webster: {names_str})"

    return {
        "driving_time_s": driving_time_s,
        "driving_time_mins": driving_mins,
        "total_signal_delay_s": total_signal_s,
        "total_eta_s": total_eta_s,
        "total_eta_mins": total_eta_mins,
        "intersections": signal_delays,
        "breakdown_text": breakdown_text,
    }

"""Define battery utilities."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ecowitt2mqtt.backports.enum import StrEnum
from ecowitt2mqtt.const import DATA_POINT_GLOB_VOLT, ELECTRIC_POTENTIAL_VOLT, PERCENTAGE
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt


class BatteryStrategy(StrEnum):
    """Define types of battery configuration."""

    BOOLEAN = "boolean"
    NUMERIC = "numeric"
    PERCENTAGE = "percentage"


class BooleanBatteryState(StrEnum):
    """Define types of battery configuration."""

    OFF = "OFF"
    ON = "ON"


def calculate_battery(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate a battery value."""
    if not (strategy := ecowitt.config.battery_overrides.get(payload_key)):
        strategy = ecowitt.config.default_battery_strategy

    if strategy == BatteryStrategy.NUMERIC or data_point_key == DATA_POINT_GLOB_VOLT:
        return CalculatedDataPoint(
            data_point_key=data_point_key, value=value, unit=ELECTRIC_POTENTIAL_VOLT
        )
    if strategy == BatteryStrategy.PERCENTAGE:
        return CalculatedDataPoint(
            data_point_key=data_point_key, value=value, unit=PERCENTAGE
        )
    if value == 0.0:
        return CalculatedDataPoint(
            data_point_key=data_point_key, value=BooleanBatteryState.OFF
        )
    return CalculatedDataPoint(
        data_point_key=data_point_key, value=BooleanBatteryState.ON
    )

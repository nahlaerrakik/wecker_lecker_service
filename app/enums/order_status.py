from enum import Enum
from typing import List


class OrderStatus(Enum):
    PLACED = "PLACED"
    PROCESSING = "PROCESSING"
    DISPATCHED = "DISPATCHED"
    DELIVERED = "DELIVERED"
    UNKNOWN = "UNKNOWN"

    @staticmethod
    def from_string(value: str) -> "OrderStatus":
        if value == OrderStatus.PLACED.value:
            return OrderStatus.PLACED

        elif value == OrderStatus.PROCESSING.value:
            return OrderStatus.PROCESSING

        elif value == OrderStatus.DISPATCHED.value:
            return OrderStatus.DISPATCHED

        elif value == OrderStatus.DELIVERED.value:
            return OrderStatus.DELIVERED

        else:
            return OrderStatus.UNKNOWN

    @staticmethod
    def list_values() -> List[str]:
        return [
            "PLACED",
            "PROCESSING",
            "DISPATCHED",
            "DELIVERED",
        ]

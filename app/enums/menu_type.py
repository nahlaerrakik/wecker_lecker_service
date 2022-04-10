from enum import Enum
from typing import List


class MenuType(Enum):
    FRESH = "FRESH"
    COOKED = "COOKED"
    UNKNOWN = "UNKNOWN"

    @staticmethod
    def from_string(value: str) -> "MenuType":
        if value == MenuType.FRESH.value:
            return MenuType.FRESH

        elif value == MenuType.COOKED.value:
            return MenuType.COOKED

        else:
            return MenuType.UNKNOWN

    @staticmethod
    def list_values() -> List[str]:
        return [
            "FRESH",
            "COOKED",
        ]
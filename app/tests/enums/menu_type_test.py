from app.enums.menu_type import MenuType


def test_menu_type_from_string_valid_value():
    assert MenuType.from_string("FRESH") == MenuType.FRESH
    assert MenuType.from_string("COOKED") == MenuType.COOKED


def test_menu_type_from_string_invalid_value():
    assert MenuType.from_string("TEST") == MenuType.UNKNOWN


def test_menu_type_from_list_values():
    assert MenuType.list_values() == ["FRESH", "COOKED"]
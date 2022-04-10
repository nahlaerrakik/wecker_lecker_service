import pytest

from app.crud.category import insert_category
from app.crud.menu import insert_menu
from app.crud.menu import query_menu
from app.crud.menu import query_menus
from app.crud.menu import query_menus_by_category
from app.schemas.category import CategoryCreate
from app.schemas.menu import MenuCreate


@pytest.fixture
def mock_category(session):
    return insert_category(db=session, category=CategoryCreate(name="category"))


@pytest.fixture
def mock_menu_list(session, mock_category):
    menu1 = insert_menu(
        db=session,
        menu=MenuCreate(
            name="menu1",
            short_description="short_description1",
            full_description="full_description1",
            price=1.0, image="image1",
            category_id=mock_category.id
        )
    )
    menu2 = insert_menu(
        db=session,
        menu=MenuCreate(
            name="menu2",
            short_description="short_description2",
            full_description="full_description2",
            price=2.0, image="image2",
            category_id=mock_category.id
        )
    )
    menu3 = insert_menu(
        db=session,
        menu=MenuCreate(
            name="menu3",
            short_description="short_description3",
            full_description="full_description3",
            price=3.0, image="image3",
            category_id=mock_category.id
        )
    )

    return [menu1, menu2, menu3]


def test_insert_menu(session, mock_category):
    menu1 = MenuCreate(
        name="menu1",
        short_description="short_description1",
        full_description="full_description1",
        price=10.0,
        image="image1",
        category_id=mock_category.id,
    )

    result = insert_menu(db=session, menu=menu1)
    assert result.id == 1
    assert result.name == "menu1"
    assert result.short_description == "short_description1"
    assert result.full_description == "full_description1"
    assert result.price == 10
    assert result.image == "image1"
    assert result.category_id == mock_category.id

    menu2 = MenuCreate(
        name="menu2",
        short_description="short_description2",
        full_description="full_description2",
        price=20,
        image="image2",
        category_id=mock_category.id,
    )
    result = insert_menu(db=session, menu=menu2)
    assert result.id == 2
    assert result.name == "menu2"
    assert result.short_description == "short_description2"
    assert result.full_description == "full_description2"
    assert result.price == 20.0
    assert result.image == "image2"
    assert result.category_id == mock_category.id


def test_query_menus_multiple_result(session, mock_menu_list):
    result = query_menus(db=session)
    assert len(result) == 3
    assert result == mock_menu_list


def test_query_menus_with_no_existent_menus(session):
    result = query_menus(db=session)
    assert len(result) == 0
    assert result == []


def test_query_menus_with_skip(session):
    result = query_menus(db=session, skip=1)
    assert len(result) == 0
    assert result == []


def test_query_menus_with_limit(session):
    result = query_menus(db=session, limit=1)
    assert len(result) == 0
    assert result == []


def test_query_menus_with_skip_and_limit(session):
    result = query_menus(db=session, skip=1, limit=1)
    assert len(result) == 0
    assert result == []


def test_query_menu(session):
    category_id = insert_category(db=session, category=CategoryCreate(name="category")).id
    menu = insert_menu(
        db=session,
        menu=MenuCreate(
            name="menu",
            short_description="short_description",
            full_description="full_description",
            price=1.0,
            image="image",
            category_id=category_id
        )
    )

    result = query_menu(db=session, menu_id=menu.id)
    assert result.id == menu.id
    assert result.name == menu.name
    assert result.short_description == menu.short_description
    assert result.full_description == menu.full_description
    assert result.price == menu.price
    assert result.image == menu.image
    assert result.category_id == menu.category_id


def test_query_menu_with_non_existent_menu(session):
    result = query_menu(db=session, menu_id=-1)
    assert result is None


def test_query_menus_by_category(session, mock_category, mock_menu_list):
    result = query_menus_by_category(db=session, category_id=mock_category.id)
    assert len(result) == 3
    assert result == mock_menu_list


def test_query_menus_by_category_with_non_existent_category(session):
    result = query_menus_by_category(db=session, category_id=-1)
    assert len(result) == 0
    assert result == []


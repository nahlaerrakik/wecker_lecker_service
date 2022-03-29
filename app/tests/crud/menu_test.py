from app.crud.category import insert_category
from app.crud.menu import insert_menu
from app.crud.menu import query_menu
from app.crud.menu import query_menus
from app.schemas.category import CategoryCreate
from app.schemas.menu import MenuCreate


def test_insert_menu(session):
    category_id = insert_category(db=session, category=CategoryCreate(name="category")).id

    menu1 = MenuCreate(
        name="menu1",
        description="description1",
        price=10.0,
        image="image1",
        category_id=category_id,
    )

    result = insert_menu(db=session, menu=menu1)
    assert result.id == 1
    assert result.name == "menu1"
    assert result.description == "description1"
    assert result.price == 10
    assert result.image == "image1"
    assert result.category_id == category_id

    menu2 = MenuCreate(
        name="menu2",
        description="description2",
        price=20,
        image="image2",
        category_id=category_id,
    )
    result = insert_menu(db=session, menu=menu2)
    assert result.id == 2
    assert result.name == "menu2"
    assert result.description == "description2"
    assert result.price == 20.0
    assert result.image == "image2"
    assert result.category_id == category_id


def test_query_menus_multiple_result(session):
    category_id = insert_category(db=session, category=CategoryCreate(name="category")).id

    menu1 = insert_menu(
        db=session,
        menu=MenuCreate(name="menu1", description="description1", price=1.0, image="image1", category_id=category_id)
    )
    menu2 = insert_menu(
        db=session,
        menu=MenuCreate(name="menu2", description="description2", price=2.0, image="image2", category_id=category_id)
    )
    menu3 = insert_menu(
        db=session,
        menu=MenuCreate(name="menu3", description="description3", price=3.0, image="image3", category_id=category_id)
    )

    result = query_menus(db=session)
    assert len(result) == 3
    assert result == [menu1, menu2, menu3]


def test_query_menus_empty_result(session):
    result = query_menus(db=session)
    assert len(result) == 0
    assert result == []

    result = query_menus(db=session, skip=1)
    assert len(result) == 0
    assert result == []

    result = query_menus(db=session, limit=1)
    assert len(result) == 0
    assert result == []

    result = query_menus(db=session, skip=1, limit=1)
    assert len(result) == 0
    assert result == []


def test_query_menu(session):
    category_id = insert_category(db=session, category=CategoryCreate(name="category")).id
    menu = insert_menu(
        db=session,
        menu=MenuCreate(name="menu", description="description", price=1.0, image="image", category_id=category_id)
    )

    result = query_menu(db=session, menu_id=menu.id)
    assert result.id == menu.id
    assert result.name == menu.name
    assert result.description == menu.description
    assert result.price == menu.price
    assert result.image == menu.image
    assert result.category_id == menu.category_id


def test_query_menu_non_existent_menu(session):
    result = query_menu(db=session, menu_id=-1)
    assert result is None

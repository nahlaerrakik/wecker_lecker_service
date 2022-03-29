from app.models.catgeory import Category
from app.models.menu import Menu


def test_create_menu(client, mocker):
    mocker.patch('app.routes.menu.query_category', return_value=Category(id=100))
    mocked_menu = Menu(id=1, name="menu", description="description", price=1.0, image="image", category_id=100)
    mocker.patch('app.routes.menu.insert_menu', return_value=mocked_menu)

    response = client.post(
        url="/menus",
        json={
            "name": "menu",
            "description": "description",
            "price": 1.0,
            "image": "image",
            "category_id": 100,
        }
    )
    assert response.status_code == 200

    result = response.json()
    assert result.get("id") == mocked_menu.id
    assert result.get("name") == mocked_menu.name
    assert result.get("description") == mocked_menu.description
    assert result.get("price") == mocked_menu.price
    assert result.get("image") == mocked_menu.image
    assert result.get("category_id") == mocked_menu.category_id


def test_create_menu_with_non_existent_category(client, mocker):
    mocker.patch('app.routes.menu.query_category', return_value=None)

    response = client.post(
        url="/menus",
        json={
            "name": "menu",
            "description": "description",
            "price": 1.0,
            "image": "image",
            "category_id": 100,
        }
    )
    assert response.status_code == 400

    result = response.json()
    assert result == {"detail": "Invalid request. Category with id 100 not found"}


def test_get_menus_multiple_result(client, mocker):
    mocked_menu_list = [
        Menu(id=1, name="menu1", description="description1", price=1.0, image="image1", category_id=100),
        Menu(id=2, name="menu2", description="description2", price=2.0, image="image2", category_id=100),
    ]
    mocker.patch('app.routes.menu.query_menus', return_value=mocked_menu_list)

    response = client.get(url="/menus")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 2
    assert result == [
        dict(id=1, name="menu1", description="description1", price=1.0, image="image1", category_id=100),
        dict(id=2, name="menu2", description="description2", price=2.0, image="image2", category_id=100),
    ]


def test_get_menus_empty_result(client, mocker):
    mocker.patch('app.routes.menu.query_menus', return_value=[])

    response = client.get("/menus")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 0
    assert result == []


def test_get_menu(client, mocker):
    mocked_menu = Menu(id=1, name="menu", description="description", price=10.0, image="image", category_id=2)
    mocker.patch('app.routes.menu.query_menu', return_value=mocked_menu)

    response = client.get("/menus/1")
    assert response.status_code == 200

    result = response.json()
    assert result == dict(id=1, name="menu", description="description", price=10.0, image="image", category_id=2)


def test_get_menu_not_found(client, mocker):
    mocker.patch('app.routes.menu.query_menu', return_value=None)

    response = client.get(url=f"/menus/1")
    assert response.status_code == 404

    result = response.json()
    assert result == {"detail": "Menu with 1 not found"}

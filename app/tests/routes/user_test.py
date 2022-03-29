import json

from app.models.user import User


def test_create_user(client, mocker):
    mocked_user = User(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        password="joedoe",
    )
    mocker.patch('app.routes.user.insert_user', return_value=mocked_user)
    mocker.patch('app.routes.user.get_password_hash', return_value="mocked_hashed_password")

    response = client.post(
        url="/users",
        json={
            "email": "joe@doe.com",
            "first_name": "joe",
            "last_name": "doe",
            "password": "joedoe",
        }
    )
    assert response.status_code == 200

    result = response.json()
    assert result.get("email") == mocked_user.email
    assert result.get("first_name") == mocked_user.first_name
    assert result.get("last_name") == mocked_user.last_name
    assert result.get("created_on") == mocked_user.created_on
    assert result.get("updated_on") == mocked_user.updated_on


def test_create_user_already_exist(client, mocker):
    mocked_existent_user = User(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        password="joedoe",
    )
    mocker.patch('app.routes.user.query_user', return_value=mocked_existent_user)

    response = client.post(
        url="/users",
        json={
            "email": "joe@doe.com",
            "first_name": "joe",
            "last_name": "doe",
            "password": "joedoe",
        }
    )
    assert response.status_code == 400

    result = response.json()
    assert result == {"detail": "User joe@doe.com already exists"}


def test_login(client, mocker):
    mocked_user = User(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        password="joedoe",
    )
    mocker.patch('app.routes.user.authenticate_user', return_value=mocked_user)
    mocker.patch('app.routes.user.create_access_token', return_value="token")
    mocker.patch('app.routes.user.update_user', return_value=None)

    response = client.post(
        url="/token",
        data={
            "username": "joe@doe.com",
            "password": "joedoe",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200

    result = response.json()
    assert result == {"access_token": "token", "token_type": "bearer"}


def test_login_with_invalid_credentials(client, mocker):
    mocker.patch('app.routes.user.authenticate_user', return_value=False)

    response = client.post(
        url="/token",
        data={
            "username": "joe@doe.com",
            "password": "joedoe",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401

    result = response.json()
    assert result == {"detail": "Incorrect username or password"}

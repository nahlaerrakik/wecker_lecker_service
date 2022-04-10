import pytest

from app.models.user import User


@pytest.fixture
def mock_user():
    return User(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        password="joedoe",
    )


def test_create_user(client, mock_user, mocker):
    mocker.patch('app.routes.user.insert_user', return_value=mock_user)
    mocker.patch('app.routes.user.get_password_hash', return_value="mocked_hashed_password")

    response = client.post(
        url="/api/v1/users/register",
        json={
            "email": "joe@doe.com",
            "first_name": "joe",
            "last_name": "doe",
            "password": "joedoe",
        }
    )
    assert response.status_code == 201

    result = response.json()
    assert result.get("email") == mock_user.email
    assert result.get("first_name") == mock_user.first_name
    assert result.get("last_name") == mock_user.last_name
    assert result.get("created_on") == mock_user.created_on
    assert result.get("updated_on") == mock_user.updated_on


def test_create_user_already_exist(client, mock_user, mocker):
    mocker.patch('app.routes.user.query_user', return_value=mock_user)

    response = client.post(
        url="/api/v1/users/register",
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


def test_login(client, mock_user, mocker):
    mocker.patch('app.routes.user.authenticate_user', return_value=mock_user)
    mocker.patch('app.routes.user.create_access_token', return_value="token")
    mocker.patch('app.routes.user.update_user', return_value=None)

    response = client.post(
        url="/api/v1/login",
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
        url="/api/v1/login",
        data={
            "username": "joe@doe.com",
            "password": "joedoe",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401

    result = response.json()
    assert result == {"detail": "Incorrect username or password"}

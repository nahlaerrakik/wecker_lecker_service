from app.crud.user import insert_user, update_user
from app.crud.user import query_user
from app.crud.user import query_users
from app.schemas.user import UserCreate, UserUpdate


def test_insert_user(session):
    user1 = UserCreate(
        email="joe@doe.com",
        first_name="joe",
        last_name="doe",
        password="joedoe",
    )

    result = insert_user(db=session, user=user1)
    assert result.email == user1.email
    assert result.first_name == user1.first_name.capitalize()
    assert result.last_name == user1.last_name.upper()
    assert result.password == user1.password

    user2 = UserCreate(
        email="jane@doe.com",
        first_name="jane",
        last_name="doe",
        password="janedoe",
    )
    result = insert_user(db=session, user=user2)
    assert result.email == user2.email
    assert result.first_name == user2.first_name.capitalize()
    assert result.last_name == user2.last_name.upper()
    assert result.password == user2.password


def test_query_users_multiple_result(session):
    user1 = insert_user(
        db=session,
        user=UserCreate(email="joe@doe.com", first_name="joe", last_name="doe", password="joedoe", )
    )
    user2 = insert_user(
        db=session,
        user=UserCreate(email="jane@doe.com", first_name="jane", last_name="doe", password="janedoe", )
    )

    user1.first_name = user1.first_name.capitalize()
    user1.last_name = user1.first_name.upper()

    user2.first_name = user2.first_name.capitalize()
    user2.last_name = user2.first_name.upper()

    result = query_users(db=session)
    assert len(result) == 2
    assert result == [user1, user2]


def test_query_users_empty_result(session):
    result = query_users(db=session)
    assert len(result) == 0
    assert result == []

    result = query_users(db=session, skip=1)
    assert len(result) == 0
    assert result == []

    result = query_users(db=session, limit=1)
    assert len(result) == 0
    assert result == []

    result = query_users(db=session, skip=1, limit=1)
    assert len(result) == 0
    assert result == []


def test_query_user_non_existent_user(session):
    result = query_user(db=session, email="notfound@email.com")
    assert result is None


def test_update_user_first_name(session):
    user = insert_user(
        db=session,
        user=UserCreate(email="joe@doe.com", first_name="joe", last_name="doe", password="joedoe", )
    )

    user_update = UserUpdate(email=user.email, first_name="test")
    result = update_user(db=session, user=user_update)

    assert result.email == user.email
    assert result.first_name == "Test"
    assert result.last_name == user.last_name.upper()
    assert result.password == user.password
    assert result.is_active is False


def test_update_user_last_name(session):
    user = insert_user(
        db=session,
        user=UserCreate(email="joe@doe.com", first_name="joe", last_name="doe", password="joedoe", )
    )

    user_update = UserUpdate(email=user.email, last_name="test")
    result = update_user(db=session, user=user_update)

    assert result.email == user.email
    assert result.first_name == user.first_name.capitalize()
    assert result.last_name == "TEST"
    assert result.password == user.password
    assert result.is_active is False


def test_update_user_password(session):
    user = insert_user(
        db=session,
        user=UserCreate(email="joe@doe.com", first_name="joe", last_name="doe", password="joedoe", )
    )

    user_update = UserUpdate(email=user.email, password="test")
    result = update_user(db=session, user=user_update)

    assert result.email == user.email
    assert result.first_name == user.first_name.capitalize()
    assert result.last_name == user.last_name.upper()
    assert result.password == "test"
    assert result.is_active is False


def test_update_user_is_active(session):
    user = insert_user(
        db=session,
        user=UserCreate(email="joe@doe.com", first_name="joe", last_name="doe", password="joedoe", )
    )

    user_update = UserUpdate(email=user.email, is_active=True)
    result = update_user(db=session, user=user_update)

    assert result.email == user.email
    assert result.first_name == user.first_name.capitalize()
    assert result.last_name == user.last_name.upper()
    assert result.password == user.password
    assert result.is_active is True


def test_update_user_with_non_existent_user(session):
    user_update = UserUpdate(email="joe@doe.com")
    assert update_user(db=session, user=user_update) is None

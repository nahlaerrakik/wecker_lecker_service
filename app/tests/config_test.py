import pytest

from app.config import Config, DB


def test_get_db_config_dev():
    config = Config(env="dev")
    db_config = config.get_db_config()
    assert db_config == DB(hostname="localhost", database="dev", username="postgres", password="admin", port=5432,)


def test_get_db_config_test():
    config = Config(env="test")
    db_config = config.get_db_config()
    assert db_config == DB(hostname="localhost", database="test", username="postgres", password="admin", port=5432,)


def test_get_db_config_prod():
    config = Config(env="prod")
    db_config = config.get_db_config()
    assert db_config == DB(hostname="localhost", database="prod", username="postgres", password="admin", port=5432,)


def test_get_db_config_with_invalid_env():
    config = Config(env="dummy")
    with pytest.raises(Exception):
        config.get_db_config()

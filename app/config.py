from typing import Any

from pydantic import BaseModel
from pydantic.tools import lru_cache


class DB(BaseModel):
    hostname: str
    database: str
    username: str
    password: str
    port: int


class Config:
    def __init__(self, env: str, **values: Any):
        super().__init__(**values)
        self.env = env
        self.dev = "dev"
        self.test = "test"
        self.prod = "prod"

    def get_db_config(self):
        if self.env == self.dev:
            return DB(
                hostname="localhost",
                database="dev",
                username="postgres",
                password="admin",
                port=5432,
            )
        elif self.env == self.test:
            return DB(
                hostname="localhost",
                database="test",
                username="postgres",
                password="admin",
                port=5432,
            )
        elif self.env == self.prod:
            return DB(
                hostname="localhost",
                database="prod",
                username="postgres",
                password="admin",
                port=5432,
            )
        else:
            raise Exception


@lru_cache()
def config(env: str) -> Config:
    return Config(env=env)


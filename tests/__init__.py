import unittest

from tortoise import Tortoise


class BasicTestCase(unittest.IsolatedAsyncioTestCase):

    config = {
        "connections": {"default": "sqlite://:memory:"},
        "apps": {
            "models": {
                "models": ["tortoise_data_migration.models", "tests.models"],
                "default_connection": "default",
            },
        },
    }

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()

        await Tortoise.init(config=self.config)

        await Tortoise.generate_schemas(safe=True)

    async def asyncTearDown(self) -> None:
        await super().asyncTearDown()

        await Tortoise.close_connections()

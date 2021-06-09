from tests import BasicTestCase
from tests.models import Configuration
from tortoise_data_migration import UpgradeMigrationError, upgrade


class UpgradeTestCase(BasicTestCase):
    async def test_simple_migration(self):
        self.assertIsNone(await Configuration.get_or_none(id="my_key"))

        self.assertTrue(await upgrade(base_package="tests.data_migrations"))

        my_key = await Configuration.get(id="my_key")

        self.assertEqual(my_key.id, "my_key")
        self.assertEqual(my_key.value, "my_value")

        my_other_key = await Configuration.get(id="my_other_key")
        self.assertEqual(my_other_key.id, "my_other_key")
        self.assertEqual(my_other_key.value, "my_other_value")

        self.assertFalse(
            await upgrade(base_package="tests.data_migrations"), "Nothing to upgrade!"
        )

    async def test_failed_migrations(self):
        with self.assertRaises(expected_exception=UpgradeMigrationError):
            await upgrade(base_package="tests.wrong_data_migrations")

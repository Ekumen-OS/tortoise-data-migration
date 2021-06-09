import unittest

from tortoise_data_migration import DataMigration


class ModelTestCase(unittest.TestCase):
    def test_name(self):
        name = "001-first-migration"
        migration = DataMigration(name=name)
        self.assertEqual(migration.name, name)

    def test_name_and_id(self):
        name = "002-second-migration"
        migration = DataMigration(id=4, name=name)
        self.assertEqual(migration.id, 4)
        self.assertEqual(migration.name, name)

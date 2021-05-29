import unittest

from data_migration import DataMigration


class ModelTestCase(unittest.TestCase):
    def test_something(self):
        name = "001-first-migration"
        migration = DataMigration(name=name)
        self.assertEqual(migration.name, name)


if __name__ == "__main__":
    unittest.main()

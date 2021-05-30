import importlib.util
import logging
import os
import re
import typing

from tortoise.transactions import in_transaction

from tortoise_data_migration.models import DataMigration

logger = logging.getLogger(__name__)


class Migration:
    def __init__(self, name: str, package: str):
        self.__name = name
        self.__package = package

    @property
    def name(self):
        return self.__name

    @property
    def module_name(self):
        return f"{self.__package}.{self.__name}"

    async def upgrade(self):
        module = importlib.import_module(self.module_name)
        await module.upgrade()

        await DataMigration.create(name=self.name)

    def __repr__(self):
        return f"Migration(name={self.__name}"


def get_available_migrations(dir_name: str) -> typing.List[Migration]:
    """Returns a list of available migrations (already applied or not)"""
    migrations = []
    for file_name in os.listdir(dir_name):
        match = re.search(r"(\d+_.*)\.py$", file_name)
        if not match:
            continue

        package_name = dir_name.replace("/", ".")
        migration = Migration(name=match.group(1), package=package_name)
        migrations.append(migration)
        logger.debug(f"Found migration {migration.module_name}")
    return migrations


async def get_pending_migrations(dir_name: str) -> typing.List[Migration]:
    """Returns a list of pending migrations"""
    pending_migrations = []
    for migration in get_available_migrations(dir_name):
        if await DataMigration.exists(name=migration.name):
            logger.debug(f"Migration {migration.name} already applied")
        else:
            logger.debug(f"Migration {migration.name} needs to be applied")
            pending_migrations.append(migration)

    return pending_migrations


async def upgrade(
    base_package: str = "data_migrations", connection_name: str = "default"
) -> bool:
    """Atomically applies all the pending data migrations available. Returns
    True if migrations were applied. False if there was nothing to do.
    Exceptions raised while applying the migrations are to be handled by the
    caller"""

    migrations = await get_pending_migrations(base_package)

    if not migrations:
        logger.info("No migrations need to be applied")
        return False

    async with in_transaction(connection_name=connection_name):
        for migration in migrations:
            logger.debug(f"Applying migration {migration.name}")
            await migration.upgrade()
            logger.debug(f"Migration {migration.name} successfully applied!")

        logger.debug(f"Successfully applied migrations: {len(migrations)}")
        return True

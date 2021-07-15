import importlib
import logging
import os
import re
import typing

from tortoise.transactions import in_transaction

from tortoise_data_migration.exception import UpgradeMigrationError
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
        return f"Migration(name={self.__name}, package={self.__package})"


def get_available_migrations(base_package: str) -> typing.List[Migration]:
    """Returns a list of available migrations (already applied or not)"""

    logger.debug(f"Looking for available migrations within {base_package}")
    migrations = []
    base_module = importlib.import_module(base_package)
    path = base_module.__path__[0]  # type: ignore  # mypy issue #1422
    for file_name in os.listdir(path):
        match = re.search(r"(\d+_.*)\.py$", file_name)
        if not match:
            continue

        migration = Migration(name=match.group(1), package=base_package)
        migrations.append(migration)
        logger.debug(f"Found migration {migration.module_name}")
    return sorted(migrations, key=lambda m: m.module_name)


async def get_pending_migrations(base_package: str) -> typing.List[Migration]:
    """Returns a list of pending migrations"""
    pending_migrations = []
    for migration in get_available_migrations(base_package):
        if await DataMigration.exists(name=migration.name):
            logger.debug(f"Migration {migration} already applied")
        else:
            logger.info(f"Migration {migration} needs to be applied")
            pending_migrations.append(migration)

    return pending_migrations


async def upgrade(
    base_package: str = "data_migrations", connection_name: str = "default"
) -> bool:
    """Atomically applies all the pending data migrations available. Returns
    True if migrations were applied. False if there was nothing to do. If
    there is an exception running a migration, UpgradeMigrationError is
    raised and should be handled by the caller"""

    migrations = await get_pending_migrations(base_package)

    if not migrations:
        logger.info("No migrations need to be applied")
        return False

    async with in_transaction(connection_name=connection_name):
        for migration in migrations:
            logger.debug(f"Applying {migration}")
            try:
                await migration.upgrade()
            except Exception as e:
                logger.exception(f"Failed to apply {migration}")
                raise UpgradeMigrationError() from e
            logger.debug(f"Migration {migration.name} successfully applied!")

        logger.debug(f"Successfully applied migrations: {len(migrations)}")
        return True

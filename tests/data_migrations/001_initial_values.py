from tests.models import Configuration


async def upgrade():
    await Configuration.create(id="my_key", value="my_value")

from tests.models import Configuration


async def upgrade():
    await Configuration.create(id="my_other_key", value="my_other_value")

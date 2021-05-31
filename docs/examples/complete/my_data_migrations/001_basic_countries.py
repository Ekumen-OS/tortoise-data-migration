from app.models import Country


async def upgrade():
    await Country.create(code="AR", name="Argentina")
    await Country.create(code="BR", name="Brazil")
    await Country.create(code="US", name="United States")

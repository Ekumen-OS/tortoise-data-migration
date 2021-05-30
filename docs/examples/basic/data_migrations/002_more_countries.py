from app.models import Country


async def upgrade():
    await Country.create(code="ZA", name="South Africa")
    await Country.create(code="GB", name="United Kingdom")

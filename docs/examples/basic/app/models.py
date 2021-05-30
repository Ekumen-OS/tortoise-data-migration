from tortoise import Model, fields


class Country(Model):
    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=2)
    name = fields.CharField(max_length=64)

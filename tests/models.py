from tortoise import Model, fields


class Configuration(Model):
    id = fields.CharField(max_length=32, pk=True)
    value = fields.CharField(max_length=128)

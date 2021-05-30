from tortoise import Model, fields


class DataMigration(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128)

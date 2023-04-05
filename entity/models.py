from tortoise import fields, models

from entity.enums import HttpMethodEnum


class BaseModel(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class Project(BaseModel):
    name = fields.CharField(max_length=255, unique=True)
    description = fields.TextField(null=True)
    interfaces = fields.ReverseRelation["Interface"]
    cases = fields.ReverseRelation["Case"]


class Interface(BaseModel):
    name = fields.CharField(max_length=255)
    method = fields.CharEnumField(
        HttpMethodEnum, default=HttpMethodEnum.GET, index=True
    )
    path = fields.CharField(max_length=255, index=True)
    headers = fields.JSONField(default=None)
    description = fields.TextField(null=True)
    project = fields.ForeignKeyField(
        "models.Project", related_name="interfaces", index=True
    )


class Step(BaseModel):
    name = fields.CharField(max_length=255)
    before = fields.TextField(null=True, description="前置")
    description = fields.TextField(null=True)
    interface = fields.ForeignKeyField("models.Interface", related_name="steps")
    after = fields.TextField(null=True, description="后置")
    project = fields.ForeignKeyField("models.Project", related_name="steps")


class Case(BaseModel):
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    before = fields.TextField(null=True, description="前置")
    interface = fields.ForeignKeyField("models.Interface", related_name="cases")
    after = fields.TextField(null=True, description="后置")
    project = fields.ForeignKeyField("models.Project", related_name="cases")


class CaseStep(BaseModel):
    step = fields.ForeignKeyField("models.Step", description="步骤")
    case = fields.ForeignKeyField("models.Case", description="用例")
    order = fields.IntField(description="步骤顺序")

    class Meta:
        table = "case_step"


class Config(BaseModel):
    key = fields.CharField(max_length=255, index=True)
    value = fields.CharField(max_length=255)
    description = fields.TextField(null=True)

import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from tortoise.queryset import MODEL, QuerySet

from entity.enums import HttpMethodEnum

# 定义一个泛型类型变量
DataT = TypeVar("DataT")


# 定义一个通用响应模型
class R(GenericModel, Generic[DataT]):
    code: int = 0
    message: str = "success"
    data: DataT

    @classmethod
    def success(cls, data: DataT = None):
        return cls(data=data)

    @classmethod
    def fail(cls, message: Optional[str] = "失败", data: DataT = None):
        return cls(code=400, message=message, data=data)


# 定义扩展后的通用响应模型
class PR(R, Generic[DataT]):
    total: int

    @classmethod
    def success(cls, data: DataT = None, total: int = 0):
        return cls(data=data, total=total)

    @classmethod
    def fail(cls, message: Optional[str] = "失败", data: DataT = None):
        return cls(code=400, message=message, data=data, total=0)


class PageParam(BaseModel):
    current: int = 1
    page_size: int = Field(default=10, description="每页数据条数", alias="pageSize")

    async def page_helper(self, query: QuerySet[MODEL]):
        offset = (self.current - 1) * self.page_size
        limit = self.page_size
        data = await query.offset(offset).limit(limit).all()
        total = await query.count()
        return {"data": data, "total": total}


class SearchParam(PageParam):
    def params(self):
        """获取除父类外的类属性作为orm 查询条件、过滤掉分页参数"""
        result = {}
        for k, v in self.__dict__.items():
            if k not in PageParam().__dict__:
                result[k] = v
        return result


class TimeField(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ProjectBase(BaseModel):
    name: str = Field(...)
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class Project(ProjectBase, TimeField):
    id: int

    class Config:
        orm_mode = True


class InterfaceBase(BaseModel):
    name: str
    method: HttpMethodEnum
    path: str
    headers: Optional[dict] = None
    description: Optional[str] = None
    project_id: int = Field(alias="projectId")


class InterfaceCreate(InterfaceBase):
    pass


class InterfaceUpdate(InterfaceBase):
    pass


class Interface(InterfaceBase, TimeField):
    id: int
    project: Project

    class Config:
        orm_mode = True


class StepBase(BaseModel):
    name: str
    before: Optional[str] = None
    description: Optional[str] = None
    interface_id: int = Field(alias="interfaceId")
    after: Optional[str] = None
    project_id: int = Field(alias="projectId")


class StepCreate(StepBase):
    pass


class StepUpdate(StepBase):
    pass


class Step(StepBase, TimeField):
    id: int
    interface: Interface

    class Config:
        orm_mode = True


class CaseBase(BaseModel):
    name: str
    description: Optional[str] = None
    before: Optional[str] = None
    interface_id: int = Field(alias="interfaceId")
    after: Optional[str] = None
    project_id: int = Field(alias="projectId")


class CaseCreate(CaseBase):
    pass


class CaseUpdate(CaseBase):
    pass


class Case(CaseBase, TimeField):
    id: int
    interface: Interface
    steps: List[Step] = []

    class Config:
        orm_mode = True


class CaseStepBase(BaseModel):
    step_id: int = Field(alias="stepId")
    case_id: int = Field(alias="caseId")
    order: int


class CaseStepCreate(CaseStepBase):
    pass


class CaseStepUpdate(CaseStepBase):
    pass


class CaseStep(CaseStepBase, TimeField):
    id: int

    class Config:
        orm_mode = True


class ConfigBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None


class ConfigCreate(ConfigBase):
    pass


class ConfigUpdate(ConfigBase):
    pass


class Config(ConfigBase, TimeField):
    id: int

    class Config:
        orm_mode = True

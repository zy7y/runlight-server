from typing import List

from fastapi import APIRouter, Depends
from pydantic import Field

from entity import models, schemas


class Search(schemas.SearchParam):
    name: str = Field(default="")
    method: str = Field(default="")
    project: str = Field(default="", alias="projectName")


PR = schemas.PR
R = schemas.R
ListInterface = List[schemas.Interface]

interface = APIRouter(prefix="/interface", tags=["Interface"])

url_dir = ""


@interface.get(url_dir, summary="接口列表")
async def query_all(search: Search = Depends()) -> PR[ListInterface]:
    query = models.Interface.filter(**search.params())
    return PR.success(**await search.page_helper(query))


@interface.post(url_dir, summary="新增接口")
async def create(instance: schemas.InterfaceCreate) -> R[schemas.Interface]:
    obj = await models.Interface.create(**instance.dict(exclude_unset=True))
    return R.success(obj)


@interface.delete("/{pk}", summary="删除接口")
async def delete(pk: int) -> R:
    await models.Interface.filter(id=pk).delete()
    return R.success()


@interface.put("/{pk}", summary="修改项目")
async def update(pk: int, instance: schemas.InterfaceUpdate) -> R[schemas.Interface]:
    await models.Interface.filter(id=pk).update(**instance.dict(exclude_unset=True))
    data = await models.Interface.get(id=pk)
    return R.success(data)

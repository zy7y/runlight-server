from typing import List

from fastapi import APIRouter, Depends
from pydantic import Field

from entity import models, schemas


class Search(schemas.SearchParam):
    name__icontains: str = Field(default="", description="名称", alias="name")


PR = schemas.PR
R = schemas.R
ListProject = List[schemas.Project]

project = APIRouter(prefix="/project", tags=["Project"])

url_dir = ""


@project.get(url_dir, summary="项目列表")
async def query_all(search: Search = Depends()) -> PR[ListProject]:
    query = models.Project.filter(**search.params())
    return PR.success(**await search.page_helper(query))


@project.post(url_dir, summary="新增项目")
async def create(instance: schemas.ProjectCreate) -> R[schemas.Project]:
    obj = await models.Project.create(**instance.dict(exclude_unset=True))
    return R.success(obj)


@project.delete("/{pk}", summary="删除项目")
async def delete(pk: int) -> R:
    await models.Project.filter(id=pk).delete()
    return R.success()


@project.put("/{pk}", summary="修改项目")
async def update(pk: int, instance: schemas.ProjectUpdate) -> R[schemas.Project]:
    await models.Project.filter(id=pk).update(**instance.dict(exclude_unset=True))
    data = await models.Project.get(id=pk)
    return R.success(data)

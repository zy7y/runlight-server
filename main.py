from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from router.interface import interface
from router.project import project

app = FastAPI()

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["entity.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(project, prefix="/api")
app.include_router(interface, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=8080)

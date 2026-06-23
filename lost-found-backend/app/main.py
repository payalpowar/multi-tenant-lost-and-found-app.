from fastapi import FastAPI

from database.database import Base, engine

import models.tenant  # noqa: F401
import models.user    # noqa: F401
import models.item    # noqa: F401
import models.claim   # noqa: F401

from routers.auth import router as auth_router
from routers.tenants import router as tenants_router
from routers.users import router as users_router
from routers.items import router as items_router
from routers.claims import router as claims_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lost & Found API")

app.include_router(auth_router)
app.include_router(tenants_router)
app.include_router(users_router)
app.include_router(items_router)
app.include_router(claims_router)


@app.get("/")
def home():
    return {"message": "Lost & Found API Running"}

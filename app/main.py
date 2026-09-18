from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_db_and_tables
from .routers import reservas, usuarios


@asynccontextmanager
async def lifespan(app: FastAPI):
    # se crean las tablas al levantar la api
    create_db_and_tables()
    yield


app = FastAPI(
    title="API de Usuarios y Reservas",
    description="Actividad de Arquitectura en la Nube - FastAPI desplegado en AWS EC2",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(usuarios.router)
app.include_router(reservas.router)


@app.get("/")
def raiz():
    return {"mensaje": "API funcionando", "documentacion": "/docs"}

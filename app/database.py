from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

# la base se guarda en un archivo sqlite dentro del proyecto
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# esto lo pide sqlite cuando se usa con fastapi
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# atajo para no repetir el Depends en cada endpoint
SessionDep = Annotated[Session, Depends(get_session)]

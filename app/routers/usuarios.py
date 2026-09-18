from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from typing import Annotated

from ..database import SessionDep
from ..models import Usuario, UsuarioCreate, UsuarioPublic, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("/", response_model=UsuarioPublic)
def crear_usuario(usuario: UsuarioCreate, session: SessionDep):
    db_usuario = Usuario.model_validate(usuario)
    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)
    return db_usuario


@router.get("/", response_model=list[UsuarioPublic])
def listar_usuarios(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    usuarios = session.exec(select(Usuario).offset(offset).limit(limit)).all()
    return usuarios


@router.get("/{usuario_id}", response_model=UsuarioPublic)
def obtener_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.patch("/{usuario_id}", response_model=UsuarioPublic)
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, session: SessionDep):
    db_usuario = session.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    datos = usuario.model_dump(exclude_unset=True)
    db_usuario.sqlmodel_update(datos)
    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)
    return db_usuario


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.delete(usuario)
    session.commit()
    return {"ok": True}

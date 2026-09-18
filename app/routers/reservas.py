from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from typing import Annotated

from ..database import SessionDep
from ..models import Reserva, ReservaCreate, ReservaPublic, ReservaUpdate, Usuario

router = APIRouter(prefix="/reservas", tags=["reservas"])


@router.post("/", response_model=ReservaPublic)
def crear_reserva(reserva: ReservaCreate, session: SessionDep):
    # reviso que el usuario exista antes de guardar la reserva
    usuario = session.get(Usuario, reserva.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_reserva = Reserva.model_validate(reserva)
    session.add(db_reserva)
    session.commit()
    session.refresh(db_reserva)
    return db_reserva


@router.get("/", response_model=list[ReservaPublic])
def listar_reservas(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    reservas = session.exec(select(Reserva).offset(offset).limit(limit)).all()
    return reservas


@router.get("/{reserva_id}", response_model=ReservaPublic)
def obtener_reserva(reserva_id: int, session: SessionDep):
    reserva = session.get(Reserva, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva


@router.patch("/{reserva_id}", response_model=ReservaPublic)
def actualizar_reserva(reserva_id: int, reserva: ReservaUpdate, session: SessionDep):
    db_reserva = session.get(Reserva, reserva_id)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    datos = reserva.model_dump(exclude_unset=True)
    db_reserva.sqlmodel_update(datos)
    session.add(db_reserva)
    session.commit()
    session.refresh(db_reserva)
    return db_reserva


@router.delete("/{reserva_id}")
def eliminar_reserva(reserva_id: int, session: SessionDep):
    reserva = session.get(Reserva, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    session.delete(reserva)
    session.commit()
    return {"ok": True}

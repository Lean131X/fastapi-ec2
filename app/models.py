from sqlmodel import Field, SQLModel


# USUARIO

class UsuarioBase(SQLModel):
    nombre: str = Field(index=True)
    email: str
    telefono: str | None = None


class Usuario(UsuarioBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioPublic(UsuarioBase):
    id: int


class UsuarioUpdate(SQLModel):
    # todo opcional para poder actualizar solo un campo
    nombre: str | None = None
    email: str | None = None
    telefono: str | None = None


# RESERVA

class ReservaBase(SQLModel):
    usuario_id: int = Field(foreign_key="usuario.id")
    fecha: str
    descripcion: str
    estado: str = "pendiente"


class Reserva(ReservaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ReservaCreate(ReservaBase):
    pass


class ReservaPublic(ReservaBase):
    id: int


class ReservaUpdate(SQLModel):
    usuario_id: int | None = None
    fecha: str | None = None
    descripcion: str | None = None
    estado: str | None = None

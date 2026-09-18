# API de Usuarios y Reservas - FastAPI en AWS EC2

Actividad de la materia Arquitectura en la Nube para Tecnologias de la Informacion (UIDE).
API RESTful hecha con FastAPI y SQLModel, con operaciones CRUD para dos entidades y
desplegada en una instancia EC2 de AWS.

## Entidades

- **Usuario**: id, nombre, email, telefono
- **Reserva**: id, usuario_id, fecha, descripcion, estado

Un usuario puede tener varias reservas (relacion 1 a N). Al crear una reserva se valida
que el usuario exista.

## Endpoints

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/` | mensaje de estado |
| POST | `/usuarios/` | crear usuario |
| GET | `/usuarios/` | listar usuarios |
| GET | `/usuarios/{id}` | obtener un usuario |
| PATCH | `/usuarios/{id}` | actualizar usuario |
| DELETE | `/usuarios/{id}` | eliminar usuario |
| POST | `/reservas/` | crear reserva |
| GET | `/reservas/` | listar reservas |
| GET | `/reservas/{id}` | obtener una reserva |
| PATCH | `/reservas/{id}` | actualizar reserva |
| DELETE | `/reservas/{id}` | eliminar reserva |

La documentacion automatica esta en `/docs`.

## Estructura del proyecto

```
fastapi-ec2/
├── app/
│   ├── __init__.py
│   ├── main.py            # app FastAPI y registro de routers
│   ├── database.py        # engine, sesion y creacion de tablas
│   ├── models.py          # modelos SQLModel
│   └── routers/
│       ├── __init__.py
│       ├── usuarios.py
│       └── reservas.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Correr en local

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Luego abrir http://127.0.0.1:8000/docs

## Despliegue en AWS EC2

- Instancia: Ubuntu Server 24.04 LTS (t2.micro)
- Security Group: puerto 22 (SSH) y puerto 8000 (TCP) abiertos
- El proceso se mantiene corriendo con pm2

```bash
pm2 start venv/bin/uvicorn --name api -- app.main:app --host 0.0.0.0 --port 8000
pm2 save
```

## URL publica

http://<IP-PUBLICA>:8000/docs

# API de Usuarios y Reservas - FastAPI en AWS EC2
 
Actividad de la materia Arquitectura en la Nube para Tecnologias de la Informacion (UIDE).
API RESTful hecha con FastAPI y SQLModel, con operaciones CRUD para dos entidades y
desplegada en una instancia EC2 de AWS.
 
## URL publica
 
La API esta corriendo en:
 
- Documentacion (Swagger): http://34.207.148.254:8000/docs
- Lista de usuarios: http://34.207.148.254:8000/usuarios/
- Lista de reservas: http://34.207.148.254:8000/reservas/
## Entidades
 
- **Usuario**: id, nombre, email, telefono
- **Reserva**: id, usuario_id, fecha, descripcion, estado
Un usuario puede tener varias reservas (relacion 1 a N). Al crear una reserva se valida
que el usuario exista, si no existe devuelve 404.
 
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
 
### Ejemplo de body para crear un usuario
 
```json
{
  "nombre": "Leandro Jaramillo",
  "email": "leandjaramillo@gmail.com",
  "telefono": "0987654321"
}
```
 
### Ejemplo de body para crear una reserva
 
```json
{
  "usuario_id": 1,
  "fecha": "2026-09-20",
  "descripcion": "Reserva sala de laboratorio",
  "estado": "pendiente"
}
```
 
## Estructura del proyecto
 
La estructura sigue la seccion "Bigger Applications - Multiple Files" de la
documentacion oficial de FastAPI.
 
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
 
Cada entidad tiene su propio router con `APIRouter`, y en `main.py` se registran
con `include_router()`. Los modelos estan separados en Base / tabla / Create /
Public / Update, como muestra la documentacion de SQLModel.
 
## Tecnologias
 
- Python 3.14
- FastAPI 0.141.1
- Uvicorn 0.53.0
- SQLModel 0.0.42
- SQLite
## Correr en local
 
```bash
git clone https://github.com/Lean131X/fastapi-ec2.git
cd fastapi-ec2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
 
Luego abrir http://127.0.0.1:8000/docs
 
## Despliegue en AWS EC2
 
**Instancia**
 
- Ubuntu Server 26.04 LTS
- Tipo t3.micro
- Region us-east-1
**Security Group**
 
| Tipo | Puerto | Origen |
|------|--------|--------|
| SSH | 22 | 0.0.0.0/0 |
| TCP personalizado | 8000 | 0.0.0.0/0 |
 
**Pasos en la instancia**
 
```bash
sudo apt update
sudo apt install -y python3-venv python3-pip git
 
git clone https://github.com/Lean131X/fastapi-ec2.git
cd fastapi-ec2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
 
**Correr la API con pm2**
 
Se usa pm2 como manejador de procesos para que la API siga corriendo despues de
cerrar la sesion SSH.
 
```bash
sudo apt install -y nodejs npm
sudo npm install -g pm2
 
pm2 start venv/bin/uvicorn --name api --interpreter venv/bin/python -- app.main:app --host 0.0.0.0 --port 8000
pm2 save
pm2 startup
```
 
El `--host 0.0.0.0` es necesario para que uvicorn escuche en todas las interfaces
y la API sea accesible desde la IP publica. El `--interpreter venv/bin/python` es
necesario porque pm2 por defecto asume que el proceso es de Node.
 
**Comandos utiles de pm2**
 
```bash
pm2 list          # ver estado
pm2 logs api      # ver logs
pm2 restart api   # reiniciar
pm2 stop api      # detener
```
 

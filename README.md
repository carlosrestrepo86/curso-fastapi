## CURSO-FASTAPI

> Descripción corta del proyecto. Qué hace, para qué sirve, o por qué lo hiciste.
Este proyecto utiliza FastAPI y SQLModel para crear usuarios, planes y transacciones. Luego los usuarios pueden subscribirse a uno o varios planes. También permite consultar, editar o eliminar usarios además de otros elementos.

> Lo hice en un curso de BackEnd en platzi.

> Proyecto basado en [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/), y [SQLModel](https://sqlmodel.tiangolo.com/) para crear una API RESTful robusta y moderna.


---

## 🚀 Características

- 🔧 API construida con FastAPI
- ✅ Validación automática con Pydantic
- 🧠 ORM + Pydantic con SQLModel
- 📄 Documentación interactiva (Swagger/OpenAPI)
- 🛡️ Manejo de autenticación/autorización (si aplica)

---


## 📁 Estructura del proyecto

```bash
.
├── app/
│   ├── main.py                    # Punto de entrada de la aplicación.
│      ├── routers/                # Rutas.
│         ├── customers            # Métodos para clientes.
│         ├── invoices             # Métodos para facturas.
│         ├── plans                # Métodos para planes.
│         ├── transactions         # Métodos para transacciones.
│      ├── tests/                  # Pruebas
│         ├── tests                # Pruebas generales.
│         ├── tests_customers      # Pruebas a los clientes.
├── .env                           # Variables de entorno.
├── conftest                       # Archivo de configuración para las pruebas.
├── create_multiple_transactions   # Crear multiples transacciones en la base de datos.
├── db                             # Conexión e inicialización de la base de datos.
├── models                         # Modelos de datos
├── README.md                      # Este archivo
├── requirements.txt               # Dependencias del proyecto
└── .gitignore
```


## 🛠️ Requisitos
Python 3.13.7
pip
(Opcional) Virtualenv


## 🧪 Instalación y ejecución
1. Clona el repositorio
git clone https://github.com/carlosrestrepo86/curso-fastapi.git

2. Crea entorno virtual (opcional pero recomendado)
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

3. Instala dependencias
pip install -r requirements.txt

4. Ejecuta la app
fastapi dev app/main.py


## ⚙️ Variables de entorno

Crea un archivo .env en la raíz del proyecto con contenido como este  
USER=tu_clave  
PASSWORD=tu_contraseña


## 📬 Endpoints disponibles

Una vez corras el servidor, puedes ver la documentación interactiva en

Swagger UI: http://localhost:8000/docs


## 🧱 Tecnologías usadas

|    Tecnología    |                Descripción                 | 
|------------------|--------------------------------------------|
| FastAPI          | Framework web moderno para construir APIs  | 
| SQLModel         | ORM ligero basado en SQLAlchemy y Pydantic | 
| Pydantic         | Validación de datos basada en tipos        |
| Uvicorn          | Servidor ASGI para FastAPI                 |
| Python-dotenv    | Carga de variables de entorno desde .env   |



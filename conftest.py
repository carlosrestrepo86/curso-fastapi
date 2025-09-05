import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from db import get_session
from models import Customer

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url, 
                       connect_args={"check_same_thread": False}, # Evitar que ejecute diferentes códigos en diferentes threads
                       poolclass=StaticPool  # Creación de la base de datos temporal y en memoria
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session # yield ceder la variable a la proxima función que la este utilizando
    SQLModel.metadata.drop_all(engine) # Borrar todas las tablas de la base de datos, limpiar memoria y evitar datos viejos
    
# Crear sesion para conectarnos a la base datos de testing
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
    
# Crear fixture que cree un Customer
@pytest.fixture(name="Customer")
def customer_fixture(session: Session):
    customer_data = {
        "name": "Carlos",
        "description": "Estudiante",
        "email": "carlos@example.com",
        "age": 39
    }
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
from fastapi.testclient import TestClient

def test_client(client):
    assert type(client) == TestClient # Valida si dos valores son iguales, si no son iguales genera una excepción
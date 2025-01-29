import pytest
from app.database import DatabaseConnection
from config import TestingConfig
from app import init_app
from app.models.paciente_model import Paciente
from tests.utils import cargar_datos, eliminar_datos

@pytest.fixture
def app(autouse=True):
    app = init_app()
    app.config.from_object(TestingConfig)
    DatabaseConnection.set_config(app.config)
    cargar_datos(DatabaseConnection)
    yield app
    eliminar_datos(DatabaseConnection)
    DatabaseConnection.close_connection()

@pytest.fixture
def client(app):
    """
    Crear un cliente de prueba para la aplicación Flask.
    """
    return app.test_client()


def test_crear_turno_valido(client, capsys):
    """
    CP-003:  Validar que un paciente pueda crear un turno correctamente.
    """
    body = {
    "correo": "jd@example.com",
    "contrasena": "12345678"}
    response = client.post("/login", json=body, content_type="application/json") 
    token = response.json["access_token"]

    payload = {
        "Fecha": "2025-06-25",
        "Hora": "10:00:00",
        "Estado": "Reservado",
        "ID_Profesional": 1
    }

    response = client.post(
        "/crear_turno",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201

    turno = Paciente.obtener_turno_por_id(2)
    
    assert str(turno['fecha']) == payload['Fecha']
    assert str(turno['hora']) == payload['Hora']
    assert turno['estado'] == payload['Estado']
    assert turno['id_profesional'] == payload['ID_Profesional']

def test_modificar_disponibilidad_invalida(client):
    """
    CP-004: Validar que no se pueda reservar un turno en un horario ya ocupado por el profesional.
    """
    body = {
    "correo": "jd@example.com",
    "contrasena": "12345678"}
    response = client.post("/login", json=body, content_type="application/json") 
    token = response.json["access_token"]

    payload = {
        "Fecha": "2025-07-25",
        "Hora": "10:00:00",
        "Estado": "Reservado",
        "ID_Profesional": 1
    }

    response = client.post(
        "/crear_turno",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 409
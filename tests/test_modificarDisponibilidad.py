import pytest
from app.database import DatabaseConnection
from config import TestingConfig
from app import init_app
from app.models.disponibilidad_model import Disponibilidad
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


def test_modificar_disponibilidad_valida(client):
    """
    CP-001: Validar que se pueda registrar la disponibilidad del profesional con un formato de datos válido.
    """
    body = {
    "correo": "juan.perez@ejemplo.com",
    "contrasena": "contrasena123"}
    response = client.post("/login", json=body, content_type="application/json") 
    token = response.json[0]["access_token"]

    payload = {
        "disponibilidades": [
            {
                "dias_semana": "Lunes",
                "hora_inicio": "8:00:00",
                "hora_fin": "12:00:00"
            },
            {
                "dias_semana": "Lunes",
                "hora_inicio": "14:00:00",
                "hora_fin": "20:00:00"
            }
        ]
    }

    response = client.put(
        "/modificar_disponibilidad",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    disponibilidad = Disponibilidad.get_disponibilidad(1)

    for d,p in zip(disponibilidad, payload['disponibilidades']):    
        assert d['dias_semana'] == p['dias_semana']
        assert d['hora_inicio'] == p['hora_inicio']
        assert d['hora_fin'] == p['hora_fin']

def test_modificar_disponibilidad_invalida(client):
    """
    CP-002: Validar que el sistema detecte un cuerpo de solicitud inválido al intentar registrar la disponibilidad.
    """
    payload = {
        "disponibilidades": [
            {
                "dias_semana": "Lunes,Martes,Miércoles",
                "hora_inicio": "08:00:00"
                # Falta "hora_fin"
            }
        ]
    }

    response = client.put(
        "/modificar_disponibilidad/1",
        json=payload,
    )

    assert response.status_code == 400
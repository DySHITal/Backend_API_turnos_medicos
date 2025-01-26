import pytest
from flask import Flask, request, jsonify
from app.controllers.profesional_controller import ProfesionalController

# Crear una aplicación Flask de prueba
app = Flask(__name__)

# Ruta temporal para pruebas
@app.route('/modificarDisponibilidad/<int:id_usuario>', methods=['POST'])
def modificar_disponibilidad(id_usuario):
    return ProfesionalController.modificarDisponibilidad(id_usuario)

@pytest.fixture
def client():
    """
    Crear un cliente de prueba para la aplicación Flask.
    """
    with app.test_client() as client:
        yield client


def test_modificar_disponibilidad_valida(client):
    """
    CP-001: Validar que se pueda registrar la disponibilidad del profesional con un formato de datos válido.
    """
    payload = {
        "disponibilidades": [
            {
                "dias_semana": "Lunes,Martes,Miércoles",
                "hora_inicio": "08:00:00",
                "hora_fin": "12:00:00"
            },
            {
                "dias_semana": "Lunes,Martes,Miércoles",
                "hora_inicio": "14:00:00",
                "hora_fin": "20:00:00"
            }
        ]
    }

    response = client.post(
        "/modificarDisponibilidad/1",
        json=payload,
        headers={"Authorization": "Bearer token_valido"}
    )

    assert response.status_code == 200
    assert response.json.get("msg") == "Disponibilidad modificada exitosamente"


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

    response = client.post(
        "/modificarDisponibilidad/1",
        json=payload,
        headers={"Authorization": "Bearer token_valido"}
    )

    assert response.status_code == 400
    assert response.json.get("msg") == "Datos incompletos o formato inválido"

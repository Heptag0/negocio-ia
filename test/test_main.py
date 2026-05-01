import pytest
from main import limpiar_respuesta


def test_limpiar_respuesta():
    resultado = limpiar_respuesta("<think>pensando...</think> ```sql SELECT * FROM tabla ```")
    assert resultado == "SELECT * FROM tabla"

import pandas as pd
import pytest
from graficos import detectar_grafico


df_lineas = pd.DataFrame({"fecha": ["2024-01-01"], "total": [100]})
df_pastel = pd.DataFrame({"categoria": ["A", "B", "C"], "cantidad": [10, 20, 30]})
df_barras = pd.DataFrame({"categoria": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"], "cantidad": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]})
def test_detectar_grafico_linea():
    assert detectar_grafico(df_lineas) == "linea"

def test_detectar_grafico_pastel():
    assert detectar_grafico(df_pastel) == "pastel"

def test_detectar_grafico_barras():
    assert detectar_grafico(df_barras) == "barras"

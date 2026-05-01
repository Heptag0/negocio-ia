import pandas as pd
from clean_db import es_columna_basura

df1 = pd.DataFrame({"columna": ["valor", "valor", "valor"]})
def test_es_columna_basura_1():
    assert es_columna_basura(df1, "columna")

df2 = pd.DataFrame({"hash_interno": [None, None, None, None, "valor"]})
def test_es_columna_basura_2():
    assert es_columna_basura(df2, "hash_interno")

df3 = pd.DataFrame({"columna_a": [1, 2, 3], "columna_b": [1, 2, 3]})
def test_es_columna_basura_3():
    assert es_columna_basura(df3, "columna_a")
    assert es_columna_basura(df3, "columna_b")
import pandas as pd
import plotly.express as px

# CONFIGURACIÓN
PALABRAS_FECHA = ["fecha", "mes", "año", "dia", "semana", "trimestre", "periodo"]

ORDEN_MESES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

#  DETECCIÓN DE TIPO DE GRÁFICO
def detectar_grafico(df):
    """
    Analiza el DataFrame y decide qué tipo de gráfico es más apropiado:
    - linea: si hay columna de fecha o tiempo
    - pastel: si hay pocos datos categóricos (<=6 filas)
    - barras: en cualquier otro caso
    """
    tiene_fecha = False
    tiene_texto = False
    tiene_numerico = False

    for col in df.columns:
        if df[col].dtype == 'datetime64' or any(palabra in col.lower() for palabra in PALABRAS_FECHA):
            tiene_fecha = True
        elif df[col].dtype in ['int64', 'float64']:
            tiene_numerico = True
        elif pd.api.types.is_string_dtype(df[col]):
            tiene_texto = True

    if tiene_fecha:
        return "linea"
    elif tiene_texto and tiene_numerico and len(df) <= 6:
        return "pastel"
    elif tiene_texto and tiene_numerico:
        return "barras"
    else:
        return "barras"

#  GENERACIÓN DE GRÁFICO
def generar_grafico(df, tipo):
    """Genera el gráfico Plotly correspondiente según el tipo detectado"""

    if tipo == "barras":
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], text_auto=True)

    elif tipo == "linea":
        col_x = df.columns[0]
        if any(mes in df[col_x].values for mes in ORDEN_MESES):
            df[col_x] = pd.Categorical(df[col_x], categories=ORDEN_MESES, ordered=True)
            df = df.sort_values(col_x)
        fig = px.line(df, x=df.columns[0], y=df.columns[1], markers=True)

    elif tipo == "pastel":
        fig = px.pie(df, names=df.columns[0], values=df.columns[1], hole=0.4)

    return fig
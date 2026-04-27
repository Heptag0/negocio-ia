import re
from llm import generar_sql, corregir_sql, generar_respuesta_natural, sugerencia
from ejecutar_query import ejecutar

# ── UTILIDADES ─────────────────────────────────────────────────
def limpiar_respuesta(respuesta):
    """Limpia la respuesta del modelo eliminando bloques thinking y formato SQL"""
    respuesta = re.sub(r'<think>.*?</think>', '', respuesta, flags=re.DOTALL)
    respuesta = respuesta.strip()\
        .replace("```sql", "").replace("```", "")\
        .replace("'", "'").replace("'", "'")\
        .replace("%", "%%")
    return respuesta

# ── CONSULTA PRINCIPAL ─────────────────────────────────────────
def consultar(pregunta, modo="rapido"):
    """
    Orquesta el flujo completo de una consulta:
    1. Genera SQL a partir de la pregunta
    2. Ejecuta el SQL contra la base de datos
    3. Si falla, reintenta con autocorrección
    4. Si modo profundo, genera respuesta en lenguaje natural
    Devuelve: (respuesta_texto, resultado_df, lista_sugerencias)
    """

    # ── GENERACIÓN DE SQL ──────────────────────────────────────
    generar = generar_sql(pregunta)
    respuesta = limpiar_respuesta(generar.message.content)

    # ── DETECTAR RESPUESTA NO SQL ─────────────────────────
    if "SELECT" not in respuesta.upper():
        if "esquema actual" in respuesta.lower():
            lista_sugerencias = sugerencia(pregunta).message.content.split("|")
            return "No he podido responder, te recomiendo estas consultas:", None, lista_sugerencias
        return respuesta, None, None

    # ── EJECUCIÓN DEL SQL ──────────────────────────────────────
    try:
        resultado = ejecutar(respuesta)

    except Exception as e:
        # ── REINTENTO CON AUTOCORRECCIÓN ───────────────────────
        print(f"ERROR - Reintentando: {e}")
        respuesta_corregida = limpiar_respuesta(
            corregir_sql(pregunta, respuesta, str(e)).message.content
        )
        try:
            resultado = ejecutar(respuesta_corregida)
        except Exception as e2:
            lista_sugerencias = sugerencia(pregunta).message.content.split("|")
            return "No se ha podido responder esta consulta. Intenta reformular la pregunta.", None, lista_sugerencias

    # ── FORMATEO DEL RESULTADO ─────────────────────────────────
    resultado = resultado.round(2)
    resultado.columns = resultado.columns.str.replace("_", " ").str.title()

    # ── RESPUESTA SEGÚN MODO ───────────────────────────────────
    if modo == "profundo":
        respuesta_natural = generar_respuesta_natural(pregunta, resultado).message.content
        return respuesta_natural, resultado, None

    return None, resultado, None
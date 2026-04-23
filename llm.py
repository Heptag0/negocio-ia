import ollama
from schema import obtener_schema
from prompt import obtener_prompt

instrucciones = obtener_prompt() + obtener_schema()

def generar_sql(pregunta):
    modelo = "qwen2.5-coder:7b"
    respuesta = ollama.chat(
        model = modelo,
        messages = [{
            "role": "system",
            "content": instrucciones},
            {"role": "user",
            "content": pregunta
            }
        ]   )
    return respuesta
    
#try: 
#  resp = generar_sql("Cuales son los cinco productos mas vendidos?")
#   respuesta_real = resp.message.content
#   print(respuesta_real)
#except Exception as e:
#    print(f"Error al generar la consulta SQL: {e}")
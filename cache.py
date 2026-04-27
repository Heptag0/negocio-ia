import streamlit as st

# Funciones para manejar la caché de resultados de preguntas -----
# Funcion simple para guardar resultados en la caché usando st.session_state

def guardar_cache(pregunta, resultado):
    if "cache" not in st.session_state:
        st.session_state["cache"] = {}
    st.session_state["cache"][pregunta] = resultado

# Función para cargar resultados de la caché

def cargar_cache(pregunta):
    if "cache" not in st.session_state:
        return None 
    return st.session_state["cache"].get(pregunta, None)
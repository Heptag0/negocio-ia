# Changelog

## V1.5.0
### Mejoras
- Separación del prompt a archivo independiente (prompt.py)
- DAYNAME() y MONTHNAME() para nombres de días y meses
- Fechas relativas: "este mes", "mes pasado", "hoy", "esta semana"
- Formato de fechas DD/MM/YYYY
- Redondeo automático a 2 decimales
- Nombres de columnas en formato legible
- Departamentos definidos en el schema
- Soporte para búsqueda de productos con LIKE
- Cálculo de costo de inventario con JOIN automático

### Correcciones
- GROUP BY estricto compatible con MySQL modo estricto
- Sintaxis MySQL exclusiva, eliminada sintaxis PostgreSQL
- Columna pagado_en correctamente referenciada en venta_articulos_limpia

## V1.0.0
- Conexión a MySQL con SQLAlchemy
- Generación de SQL con LLM local via Ollama
- Interfaz web con Streamlit
- Detección de consultas vs conversación casual
- Manejo de errores amigable
- Credenciales seguras con .env
import streamlit as st
from openai import OpenAI
from io import BytesIO
import docx
import pandas as pd
from st_social_media_links import SocialMediaIcons
import os
from dotenv import load_dotenv  # Cargar variables de entorno desde el archivo .env

# Configurar la página como el primer comando
st.set_page_config(page_title="Contenido para Ciencia de Datos con GPT-4o", page_icon="🤖")

# Cargar la clave de OpenAI desde el archivo .env
load_dotenv()  # Carga la clave desde el archivo .env
openai_api_key = os.getenv("OPENAI_API_KEY")  # Obtiene la clave de la variable de entorno

# Configuración de OpenAI con la clave obtenida
client = OpenAI(api_key=openai_api_key)

# Función genérica para solicitudes a OpenAI
def generate_content(task, prompt, max_tokens=1500, temperature=0.7):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": task},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Ocurrió un error: {str(e)}")
        return None

# Función para crear archivos Word
def create_word_doc(content, title="Contenido Generado"):
    doc = docx.Document()
    doc.add_heading(title, level=0)
    doc.add_paragraph(content)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Configuración del Logo y Titulo de la App
st.image("https://cdn-icons-png.flaticon.com/512/4824/4824797.png", width=80)  # Ajusta el tamaño del logo

st.markdown(
    """
    <h1 style='text-align: center;'>SMART DATA SCIENCE</h1>
    """,
    unsafe_allow_html=True
)

# Configuración de la barra lateral
section = st.sidebar.selectbox("Selecciona una opción", ["Resúmenes Técnicos", "Código Python", "Dataset"])

# Lógica de las secciones
if section == "Resúmenes Técnicos":
    st.markdown("### Generación de Resúmenes Técnicos")
    st.markdown(
        """
        🔍 **Ejemplos de uso**:
    - (Análisis de clustering, Redes neuronales profundas, Visualización de datos, Optimización de algoritmos)
        """
    )
    topic = st.text_input("Ingrese un tema de ciencia de datos:")
    if st.button("Generar Resumen"):
        if topic:
            task = "Eres un experto en ciencia de datos. Proporciona resúmenes técnicos claros con ejemplos prácticos."
            summary = generate_content(task, f"Explica: {topic}", temperature=0.6)
            if summary:
                st.markdown(f"### Resumen sobre {topic}")
                st.markdown(summary)
                st.download_button(
                    "Descargar Resumen", 
                    data=create_word_doc(summary, title=f"Resumen sobre {topic}"), 
                    file_name="resumen_tecnico.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

elif section == "Código Python":
    st.markdown("### Generación de Codigo")
    st.markdown(
        """
        💡 **Ejemplos de uso**:
        - (Creación de gráficos, Conectar a bases de datos SQL, Web scraping de datos de precios, Crear una API REST básica con FastAPI)
        """
    )
    description = st.text_input("Describe qué código necesitas:")
    if st.button("Generar Código"):
        if description:
            task = "Eres un experto en Python. Genera código eficiente sin explicaciones adicionales."
            code = generate_content(task, f"Escribe código para: {description}", temperature=0.2)
            if code:
                st.code(code, language="python")
                st.download_button("Descargar Código", data=code, file_name="codigo.py", mime="text/plain")

elif section == "Dataset":
    st.markdown("### Generación de Dataset")
    st.markdown(
        """
        📊 **Ejemplos de uso**:
- (Datos de ventas para 2024, Clientes de e-commerce, Datos demográficos de una región, Precios de criptomonedas históricas)
        """
    )
    description = st.text_input("Describe el dataset que necesitas:")
    if st.button("Generar Dataset"):
        if description:
            task = "Genera datos en formato CSV con encabezados y al menos 100 filas."
            data = generate_content(task, f"Dataset sobre: {description}", temperature=0.5)
            if data:
                st.download_button(
                    "Descargar Dataset", 
                    data=data.encode('utf-8'), 
                    file_name="dataset.csv", 
                    mime="text/csv"
                )

# Pie de página
st.markdown(
    """
    <div style="text-align: center;">
        <strong>Desarrollador:</strong> Edwin Quintero Alzate | <strong>Email:</strong> egqa1975@gmail.com
    </div>
    """, 
    unsafe_allow_html=True
)
SocialMediaIcons([
    "https://www.facebook.com/edwin.quinteroalzate",
    "https://www.linkedin.com/in/edwinquintero0329/",
    "https://github.com/Edwin1719",
]).render()
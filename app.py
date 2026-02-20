import subprocess
import sys

# FORÇANDO A INSTALAÇÃO DA VERSÃO CORRETA NO STARTUP
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "google-generativeai==0.8.3"])
except Exception as e:
    pass

import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO

# Configuração
st.set_page_config(page_title="Portal Perito RS")
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

st.title("🚀 Portal Perito RS")

# Se o código acima funcionar, este diagnóstico vai ficar VERDE
if st.button("Rodar Diagnóstico de API"):
    try:
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_methods]
        st.success(f"Conectado! Modelos: {modelos}")
    except Exception as e:
        st.error(f"O servidor ainda está usando a biblioteca antiga: {e}")

materia = st.text_input("Matéria:")
if st.button("Gerar"):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Plano de aula para {materia}")
    st.write(response.text)

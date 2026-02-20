import subprocess
import sys

# --- CÓDIGO DE CHOQUE: FORÇA A ATUALIZAÇÃO DA BIBLIOTECA NO SERVIDOR ---
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "google-generativeai==0.8.3"])
except Exception as e:
    print(f"Erro na instalação forçada: {e}")
# ----------------------------------------------------------------------

import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO

# Configuração da Página
st.set_page_config(page_title="Portal Perito RS", layout="wide")

# Recuperação da API Key das Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Erro: GOOGLE_API_KEY não configurada nas Secrets.")

st.title("🚀 Portal Perito RS - Gerador de Planos")

# Diagnóstico
with st.expander("🔍 Rodar Diagnóstico de API"):
    if st.button("Verificar Conexão"):
        try:
            modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_methods]
            st.success("Conexão OK!")
            st.write("Modelos:", modelos)
        except Exception as e:
            st.error(f"Erro: {e}")

st.divider()

materia = st.text_input("Qual a matéria?")
ano = st.selectbox("Ano?", ["1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano"])

if st.button("Gerar Planejamento"):
    if materia:
        with st.spinner("Redigindo em Arial 12..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Plano de aula BNCC para {materia}, {ano}.")
                texto = response.text
                st.write(texto)
                
                # Word em Arial 12
                doc = Document()
                style = doc.styles['Normal']
                style.font.name = 'Arial'
                style.font.size = 12
                doc.add_paragraph(texto)
                
                buffer = BytesIO()
                doc.save(buffer)
                buffer.seek(0)
                st.download_button("📥 Baixar em Word", buffer, f"{materia}.docx")
            except Exception as e:
                st.error(f"Erro: {e}")

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
import os
from docx import Document
from io import BytesIO

# Configuração da Página
st.set_page_config(page_title="Portal Perito RS", layout="wide")

# Recuperação da API Key das Secrets do Streamlit
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Erro: GOOGLE_API_KEY não encontrada nas Secrets.")

st.title("🚀 Portal Perito RS - Gerador de Planos")

# Bloco de Diagnóstico
with st.expander("🔍 Rodar Diagnóstico de API"):
    if st.button("Verificar Conexão e Modelos"):
        try:
            # O comando supported_methods agora funcionará com a biblioteca 0.8.3
            modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_methods]
            st.success("Conexão estabelecida com sucesso!")
            st.write("Modelos disponíveis:", modelos)
        except Exception as e:
            st.error(f"Erro no Diagnóstico: {e}")

st.divider()

# Interface de Entrada
materia = st.text_input("Qual a matéria do planejamento?")
ano = st.selectbox("Para qual ano?", ["1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano"])

if st.button("Gerar Planejamento"):
    if materia:
        with st.spinner("A IA está redigindo seu plano em Arial 12..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Crie um plano de aula completo para a matéria de {materia} voltado para o {ano}, seguindo a BNCC."
                response = model.generate_content(prompt)
                
                texto_gerado = response.text
                st.subheader("Resultado Visual:")
                st.write(texto_gerado)
                
                # Gerador de Word (Arial 12)
                doc = Document()
                style = doc.styles['Normal']
                style.font.name = 'Arial'
                style.font.size = 12
                
                doc.add_heading(f'Plano de Aula: {materia} - {ano}', 0)
                doc.add_paragraph(texto_gerado)
                
                buffer = BytesIO()
                doc.save(buffer)
                buffer.seek(0)
                
                st.download_button(
                    label="📥 Baixar Plano em Word (Arial 12)",
                    data=buffer,
                    file_name=f"Plano_{materia}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                st.error(f"Erro ao gerar: {e}")
    else:
        st.warning("Por favor, digite a matéria.")

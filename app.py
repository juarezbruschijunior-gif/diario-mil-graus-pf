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
    st.error("Erro: GOOGLE_API_KEY não configurada.")

st.title("🚀 Portal Perito RS")

# Diagnóstico Simplificado (Sem o comando que dá erro)
if st.button("Rodar Diagnóstico"):
    try:
        # Apenas tenta listar os nomes, sem checar 'supported_methods'
        modelos = [m.name for m in genai.list_models()]
        st.success("Conectado com sucesso!")
        st.write("Modelos disponíveis:", modelos)
    except Exception as e:
        st.error(f"Erro na conexão: {e}")

st.divider()

materia = st.text_input("Qual a matéria?")
ano = st.selectbox("Para qual ano?", ["1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano"])

if st.button("Gerar Planejamento"):
    if materia:
        with st.spinner("Gerando plano em Arial 12..."):
            try:
                # Usa o modelo padrão que funciona em quase todas as versões
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Crie um plano de aula BNCC para {materia}, {ano}.")
                texto = response.text
                st.write(texto)
                
                # Gerador de Word
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
                st.error(f"Erro ao gerar: {e}")

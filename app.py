import streamlit as st
import pandas as pd

# 1. Configuração de Identidade e SEO
st.set_page_config(page_title="Diário Mil Graus Passo Fundo - Notícias Locais", page_icon="📰")

# Estilo Visual de Jornal Profissional
st.markdown("""
    <style>
    .main { background-color: #f4f4f4; color: #333; }
    .noticia-container { background-color: #ffffff; padding: 25px; border-radius: 5px; border-bottom: 3px solid #d32f2f; margin-bottom: 30px; box-shadow: 0px 2px 5px rgba(0,0,0,0.1); }
    h1 { color: #d32f2f; font-family: 'Playfair Display', serif; text-align: center; border-bottom: 2px solid #333; }
    h2 { color: #1a1a1a; }
    .footer { text-align: center; font-size: 0.8em; color: #666; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# Link da sua planilha formatado para leitura direta de CSV
URL_CSV = "https://docs.google.com/spreadsheets/d/1V2CGR5owvN_1LYkVrJjjxg71L1TeGzo3K8onaatZ0I8/export?format=csv"

# 2. Menu de Navegação
st.sidebar.title("📌 Editorias")
menu = st.sidebar.radio("Navegar por:", ["Últimas Notícias", "Arquivo de Notícias", "Sobre o Diário", "Privacidade"])

# --- PÁGINA PRINCIPAL: ÚLTIMAS NOTÍCIAS ---
if menu == "Últimas Notícias":
    st.title("📰 DIÁRIO MIL GRAUS PASSO FUNDO")
    st.write(f"**Data:** {pd.Timestamp.now().strftime('%d/%m/%Y')} | Acompanhe os fatos da nossa região.")
    
    try:
        df = pd.read_csv(URL_CSV)
        # Mostra as notícias da mais nova para a mais antiga
        for index, row in df.iloc[::-1].iterrows():
            with st.container():
                st.markdown("<div class='noticia-container'>", unsafe_allow_html=True)
                st.caption(f"📅 {row['Data']} | 📂 {row['Categoria']}")
                st.header(row['Titulo'])
                if pd.notna(row['Imagem_URL']):
                    st.image(row['Imagem_URL'], use_container_width=True)
                # O Google exige textos longos (mínimo 30 linhas) para aprovar
                st.write(row['Conteudo'])
                st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.info("O Diário está sendo atualizado. Em breve, as notícias de Passo Fundo estarão aqui!")

# --- PÁGINA DE ARQUIVO (NOTÍCIAS ANTIGAS) ---
elif menu == "Arquivo de Notícias":
    st.title("📂 Arquivo Histórico")
    st.write("Pesquise por fatos que marcaram Passo Fundo anteriormente.")
    try:
        df = pd.read_csv(URL_CSV)
        for index, row in df.iterrows():
            st.markdown(f"**[{row['Data']}]** - {row['Titulo']} (*{row['Categoria']}*)")
    except:
        st.write("Arquivo em fase de digitalização.")

# --- SOBRE E PRIVACIDADE ---
elif menu == "Sobre o Diário":
    st.title("👨‍💻 Nossa Missão")
    st.write("O Diário Mil Graus Passo Fundo é um portal independente liderado por Juarez Bruschi Junior, focado em jornalismo local sério e utilidade pública.")

elif menu == "Privacidade":
    st.title("🔒 Privacidade")
    st.write("Seguimos todas as normas do Google AdSense para proteção de dados.")

# Rodapé de Autoridade
st.markdown("<div class='footer'>Diário Mil Graus Passo Fundo © 2026<br>Passo Fundo - Rio Grande do Sul</div>", unsafe_allow_html=True)

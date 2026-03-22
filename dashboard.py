# =============================================================================
# dashboard.py
# Dashboard interativo para visualização das vagas coletadas.
# Execute com: streamlit run dashboard.py
# =============================================================================

import pandas as pd
import streamlit as st

# --- Configuração da página ---
st.set_page_config(
    page_title="Vagas de Python — Dashboard",
    page_icon="🐍",
    layout="wide"
)

# --- Carrega os dados ---
@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/vagas.csv")
    df = df.fillna("Não informado")
    return df

df = carregar_dados()

# --- Cabeçalho ---
st.title("🐍 Vagas de Python no Brasil")
st.markdown("Dados coletados automaticamente do **Vagas.com.br** via Web Scraping com Python.")
st.divider()

# --- Métricas do topo ---
col1, col2, col3 = st.columns(3)
col1.metric("Total de Vagas", len(df))
col2.metric("Empresas diferentes", df["empresa"].nunique())
col3.metric("Cidades/modalidades", df["local"].nunique())

st.divider()

# --- Filtros na barra lateral ---
st.sidebar.header("Filtros")

niveis = ["Todos"] + sorted(df["nivel"].unique().tolist())
nivel_selecionado = st.sidebar.selectbox("Nível", niveis)

locais = ["Todos"] + sorted(df["local"].unique().tolist())
local_selecionado = st.sidebar.selectbox("Localidade", locais)

busca = st.sidebar.text_input("Buscar por título ou empresa")

# --- Aplica filtros ---
df_filtrado = df.copy()

if nivel_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["nivel"] == nivel_selecionado]

if local_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["local"] == local_selecionado]

if busca:
    mask = (
        df_filtrado["titulo"].str.contains(busca, case=False, na=False) |
        df_filtrado["empresa"].str.contains(busca, case=False, na=False)
    )
    df_filtrado = df_filtrado[mask]

# --- Gráficos ---
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Vagas por nível")
    nivel_count = df_filtrado["nivel"].value_counts()
    st.bar_chart(nivel_count)

with col_g2:
    st.subheader("Top 10 localidades")
    local_count = df_filtrado["local"].value_counts().head(10)
    st.bar_chart(local_count)

st.divider()

# --- Tabela de vagas ---
st.subheader(f"Vagas encontradas ({len(df_filtrado)})")

# Transforma o link em âncora clicável
df_exibir = df_filtrado.copy()
df_exibir["link"] = df_exibir["link"].apply(
    lambda url: f'<a href="{url}" target="_blank">Ver vaga</a>'
)

st.write(
    df_exibir.to_html(escape=False, index=False),
    unsafe_allow_html=True
)
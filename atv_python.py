import pandas as pd
import streamlit as st
import plotly.express as px
from typing import Optional

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard de Vendas E-Commerce",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CAMADA DE DADOS ---
@st.cache_data
def carregar_dados(caminho_arquivo: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(caminho_arquivo)
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
        return df
    except FileNotFoundError:
        st.error(f"Erro: Arquivo '{caminho_arquivo}' não encontrado. Execute o ETL primeiro.")
        return pd.DataFrame()

# --- CAMADA DE LÓGICA E FILTROS ---
def filtrar_dados(df: pd.DataFrame, ano_selecionado: int, estados_selecionados: list) -> pd.DataFrame:
    df_filtrado = df[df['ano'] == ano_selecionado]
    
    if estados_selecionados:
        df_filtrado = df_filtrado[df_filtrado['customer_state'].isin(estados_selecionados)]
        
    return df_filtrado

# --- CAMADA DE VISUALIZAÇÃO ---
def plotar_faturamento_mensal(df: pd.DataFrame):
    vendas_mensais = df.groupby('ano_mes')['valor_total'].sum().reset_index()
    vendas_mensais['ano_mes'] = vendas_mensais['ano_mes'].astype(str) # Conversão para plotagem correta
    
    fig = px.line(
        vendas_mensais, 
        x='ano_mes', 
        y='valor_total', 
        title='Evolução do Faturamento Mensal',
        markers=True,
        labels={'ano_mes': 'Mês', 'valor_total': 'Faturamento (R$)'}
    )
    # ATUALIZAÇÃO: use_container_width substituído por width='stretch' para evitar warning
    st.plotly_chart(fig, width="stretch") # type: ignore

def plotar_top_categorias(df: pd.DataFrame):
    top_categorias = df.groupby('product_category_name')['valor_total'].sum().nlargest(10).reset_index()
    
    fig = px.bar(
        top_categorias, 
        x='valor_total', 
        y='product_category_name', 
        orientation='h',
        title='Top 10 Categorias por Faturamento',
        text_auto='.2s',
        labels={'product_category_name': 'Categoria', 'valor_total': 'Total Vendido (R$)'}
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    # ATUALIZAÇÃO: use_container_width substituído por width='stretch' para evitar warning
    st.plotly_chart(fig, width="stretch") # type: ignore

def exibir_kpis(df: pd.DataFrame):
    if df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    total_vendas = df['valor_total'].sum()
    total_pedidos = df['order_id'].nunique()
    ticket_medio = total_vendas / total_pedidos if total_pedidos > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Faturamento Total", f"R$ {total_vendas:,.2f}")
    col2.metric("Total de Pedidos", f"{total_pedidos}")
    col3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

# --- FUNÇÃO PRINCIPAL ---
def main():
    st.title("📊 Dashboard de Performance de Vendas")
    st.markdown("---")

    # 1. Carregamento
    ARQUIVO_DADOS = 'dados_vendas.csv'
    df_dados = carregar_dados(ARQUIVO_DADOS)

    if df_dados.empty:
        return

    # 2. Sidebar (Filtros)
    st.sidebar.header("Filtros")
    
    lista_anos = sorted(df_dados['ano'].unique())
    ano_selecionado = st.sidebar.selectbox("Selecione o Ano", lista_anos, index=len(lista_anos)-1)

    lista_estados = sorted(df_dados['customer_state'].unique())
    estados_selecionados = st.sidebar.multiselect("Selecione o Estado (Opcional)", lista_estados)

    # 3. Filtragem
    df_filtrado = filtrar_dados(df_dados, ano_selecionado, estados_selecionados)

    # 4. Exibição
    exibir_kpis(df_filtrado)
    
    col_graf1, col_graf2 = st.columns([2, 1])
    
    with col_graf1:
        plotar_faturamento_mensal(df_filtrado)
    
    with col_graf2:
        plotar_top_categorias(df_filtrado)

if __name__ == "__main__":
    main()
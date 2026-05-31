import streamlit as st
import pandas as pd
import plotly.express as px
import utils.filtros as filtros, utils.grafico as grafico

df_filtrado, categorias, pets = filtros.interface()
categoria_grafico = categorias if categorias else ["Todos"]
pet_grafico = pets if pets else ["Todos"]

st.markdown("""
    <style>
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 0.5rem;
        padding-left: 1rem;   /* margem lateral menor */
        padding-right: 1rem;  /* margem lateral menor */
        max-width: 95% !important;   /* ocupa quase toda a largura */
    }
    .kpi-container {
        display: flex;
        flex-wrap: wrap;              /* permite reorganizar em telas menores */
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .kpi-card {
        flex: 1;
        min-width: 220px;             /* largura mínima para não quebrar fácil */
        border-radius: 12px;
        padding: 15px;
        margin: 5px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        overflow: hidden;
    }
    .kpi-icon {
        font-size: 28px;
        margin-right: 12px;
        color: #fff;
    }
    .kpi-info {
        text-align: left;
        flex-shrink: 1;               /* permite reduzir sem quebrar */
    }
    .kpi-value {
        font-size: 26px;
        font-weight: bold;
        color: #fff;
        white-space: nowrap;          /* mantém em uma linha */
        overflow: hidden;
        text-overflow: ellipsis;      /* mostra "..." se não couber */
    }
    .kpi-label {
        font-size: 14px;
        color: #f1f1f1;
        white-space: nowrap;          /* mantém em uma linha */
        overflow: hidden;
        text-overflow: ellipsis;      /* mostra "..." se não couber */
    }
    .kpi-change-up {
        color: #d4edda;
        font-weight: bold;
        font-size: 16px;
        white-space: nowrap;
    }
    .kpi-change-down {
        color: #f8d7da;
        font-weight: bold;
        font-size: 16px;
        white-space: nowrap;
    }

    /* Cores diferentes e ordem de quebra */
    .bg-red { background-color: #DD2D4A; }
    .bg-purple { background-color: #985BC1; }
    .bg-orange { background-color: #fb8500;  }
    .bg-blue { background-color: #00B4D8;  }
            
    </style>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
    <style>
    h1 {
        margin-bottom: 0rem !important;  /* diminui espaço abaixo do título */
    }

    hr {
        margin-top: -0.25rem !important;   /* aproxima a linha */
        margin-bottom: 0rem !important;  /* opcional */
    }
    
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/pet_supplies_correto.csv")
    return df

df = carregar_dados()

total_produtos = len(df_filtrado["title"])
total_produtos_formatado = f"{total_produtos:,.0f}".replace(",", ".")

# Total de vendas
total_vendas = df_filtrado["tradeAmount_num"].sum()
total_vendas_formatado = f"{total_vendas:,.0f}".replace(",", ".")

# Total de Interesse
interesse_total = df_filtrado["wishedCount"].sum()
interesse_total_formatado = f"{interesse_total:,.0f}".replace(",", ".")

# Estoque total
estoque_total = df_filtrado["quantity"].sum()
estoque_total_formatado = f"{estoque_total:,.0f}".replace(",", ".")
#top_produto = ranking_produtos.ranking.iloc[0]["title_curto"]
categoria_maior_estoque = (df_filtrado.groupby("category")["quantity"].sum().idxmax())

# Layout dos KPIs com cores diferentes
st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card bg-red">
        <div class="kpi-icon">📦</div>
        <div class="kpi-info">
            <div class="kpi-value">{total_produtos_formatado}</div>
            <div class="kpi-label">Total de Produtos</div>
            <div class="kpi-change-up">Produtos cadastrados</div>
        </div>
    </div>
    <div class="kpi-card bg-purple">
        <div class="kpi-icon">💰</div>
        <div class="kpi-info">
            <div class="kpi-value">{total_vendas_formatado}</div>
            <div class="kpi-label">Total de Vendas</div>
            <div class="kpi-change-down">Volume total vendido</div>
        </div>
    </div>
    <div class="kpi-card bg-blue">
        <div class="kpi-icon">⭐</div>
        <div class="kpi-info">
            <div class="kpi-value">{interesse_total_formatado}</div>
            <div class="kpi-label">Interesse nos Produtos</div>
            <div class="kpi-change-up">Engajamento dos clientes</div>
        </div>
    </div>
    <div class="kpi-card bg-orange">
        <div class="kpi-icon">🏬</div>
        <div class="kpi-info">
            <div class="kpi-value">{estoque_total_formatado}</div>
            <div class="kpi-label">Estoque Total</div>
            <div class="kpi-change-up">Categoria lider: {categoria_maior_estoque}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}

[data-testid="stHorizontalBlock"] {
    gap: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        
        grafico.estoque_categoria(df_filtrado, categoria_grafico)

    with st.container(border=True):
    
        grafico.estoque_pet(df_filtrado, categoria_grafico)
        
with col2:
    with st.container(border=True):
        grafico.venda_categoria_pet(df_filtrado, categoria_grafico, pet_grafico)

col3, col4 = st.columns(2)
with col3:
    with st.container(border=True):
        grafico.interesse_venda(df_filtrado, categoria_grafico)

with col4:
    with st.container(border=True):
        grafico.avaliacao_venda(df_filtrado, categoria_grafico)
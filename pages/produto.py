import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import utils.filtros as filtros, utils.grafico as grafico

st.markdown("""
    <style>
        .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        padding-left: 1rem;   /* margem lateral menor */
        padding-right: 1rem;  /* margem lateral menor */
        max-width: 95% !important;   /* ocupa quase toda a largura */
        }
        [data-testid="stVerticalBlock"] {
            gap: 0.5rem;
        }

        [data-testid="stHorizontalBlock"] {
            gap: 0.5rem;
        }
        /* tudo dentro do radio */
        div[data-testid="stRadio"] * {
            font-size: 16px !important;
        }

        /* tudo dentro do checkbox */
        div[data-testid="stCheckbox"] * {
            font-size: 16px !important;
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

        .kpi-card {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-top: 20px;

        border-radius: 16px;
        padding: 20px;

        color: white;

        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
            
        .bg-red { background-color: #DD2D4A; }
            
        /* Ícone */
        .kpi-icon {
        font-size: 40px;
        }

        /* Texto */
        .kpi-info {
            display: flex;
            flex-direction: column;
        }

        .kpi-value {
            font-size: 32px;
            font-weight: bold;
            line-height: 1.2;
        }

        .kpi-label {
            font-size: 16px;
            margin-top: 4px;
        }

        .kpi-extra {
            font-size: 18px;
            font-weight: bold;
            margin-top: 6px;
        }
            
    </style>
""", unsafe_allow_html=True)

# =====================================
# 1. DADOS
# =====================================

@st.cache_data
def carregar_dados():
    return pd.read_csv("data/pet_supplies_correto.csv")

df = carregar_dados()

# usa o filtro correto que você JÁ TEM no projeto
df_filtrado, categorias, pets = filtros.interface()

st.markdown("---")
st.markdown("""
    <style>
        h1 {
            margin-bottom: 0rem !important;  /* diminui espaço abaixo do título */
        }

        hr {
            margin-top: 0.2rem !important;   /* aproxima a linha */
            margin-bottom: 0rem !important;  /* opcional */
        }
        
    </style>
""", unsafe_allow_html=True)

# se quiser usar o filtrado, usa ele
df = df_filtrado.copy()

categoria_grafico = categorias if categorias else ["Todos"]
pet_grafico = pets if pets else ["Todos"]

# =============================
# MENU DE SELEÇÃO
# =============================
opcao = st.selectbox(
    "Escolha o ranking que deseja visualizar:",
    [
        "⭐ Melhores Avaliados",
        "💰 Mais Vendidos",
        "🔥 Mais Populares",
        "🚀 Top Geral (Score combinado)"
    ]
)

# =============================
# 1. MELHORES AVALIADOS
# =============================
top_avaliados = (
    df.groupby("title_curto")["averageStar"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_avaliados.columns = ["Produto", "Avaliação Média"]
top_avaliados.insert(0, "Ranking", range(1, len(top_avaliados) + 1))

# =============================
# 2. MAIS VENDIDOS
# =============================
top_vendidos = (
    df.groupby("title_curto")["tradeAmount_num"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_vendidos.columns = ["Produto", "Quantidade de Vendas"]
top_vendidos.insert(0, "Ranking", range(1, len(top_vendidos) + 1))

# =============================
# 3. MAIS POPULARES
# =============================
df["popularity_score"] = (
    df["quantity"] + df["wishedCount"]
)

top_populares = (
    df.groupby("title_curto")["popularity_score"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_populares.columns = ["Produto", "Score de popularidade"]
top_populares.insert(0, "Ranking", range(1, len(top_populares) + 1))

# =============================
# 4. SCORE FINAL
# =============================
df_score = df.groupby("title_curto").agg({
    "averageStar": "mean",
    "tradeAmount_num": "sum",
    "wishedCount": "sum"
}).reset_index()

df_score["score_final"] = (
    df_score["averageStar"] * 0.4 +
    np.log1p(df_score["tradeAmount_num"]) * 0.4 +
    np.log1p(df_score["wishedCount"]) * 0.2
)

top_geral = (
    df_score.sort_values("score_final", ascending=False)
    .head(10)
    .rename(columns={
        "title_curto": "Produto",
        "averageStar": "Avaliação",
        "tradeAmount_num": "Quantidade de Vendas",
        "wishedCount": "Desejos",
        "score_final": "Score Final"
    })
    
)
top_geral.insert(0, "Ranking", range(1, len(top_geral) + 1))

# =============================
# MOSTRAR APENAS UMA TABELA
# =============================
if opcao == "⭐ Melhores Avaliados":
    st.subheader(opcao)
    st.dataframe(top_avaliados, use_container_width=True, hide_index=True)

elif opcao == "💰 Mais Vendidos":
    st.subheader(opcao)
    st.dataframe(top_vendidos, use_container_width=True, hide_index=True)

elif opcao == "🔥 Mais Populares":
    st.subheader(opcao)
    st.dataframe(top_populares, use_container_width=True, hide_index=True)

elif opcao == "🚀 Top Geral (Score combinado)":
    st.subheader(opcao)
    st.dataframe(top_geral, use_container_width=True, hide_index=True)

df["wishedCount"] = pd.to_numeric(df["wishedCount"], errors="coerce").fillna(0)
df["tradeAmount_num"] = pd.to_numeric(df["tradeAmount_num"], errors="coerce").fillna(0)
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)

# -----------------------------
# LAYOUT: CONTROLES + HEATMAP
# -----------------------------

col_heat1, col_heat2 = st.columns([1, 3])

with st.container(border=True):
    col_heat1, col_heat2 = st.columns([1, 3])

# ESQUERDA -> métricas + checkbox
with col_heat1:
    st.markdown("<br><br>", unsafe_allow_html=True)  # 👈 empurra pra baixo
    
    st.markdown("""
        <div style="
            font-size: 18px;
            font-weight: bold;
            color: #3967BC;
            margin-bottom: 0.2px;
        ">
        Selecione a métrica
        </div>
        """, unsafe_allow_html=True)
    
    metric = st.radio(
        "",
        ["Quantidade de Produtos", "Quantidade Vendida", "Volume de Interesse"]
    )

    normalize = st.checkbox("Mostrar em percentual (preferência por pet)")

    col1, col2, col3 = st.columns([1,2,1])  # só pra colocar centralizado
    with col2:
        st.image("imagens/gato1.png", width=200)

# DIREITA -> heatmap
with col_heat2:
        # -----------------------------
        # DEFINIR VALORES DO HEATMAP
        # -----------------------------
        if metric == "Quantidade de Produtos":
            value_col = "title_curto"
            aggfunc = "count"

        elif metric == "Quantidade Vendida":
            value_col = "tradeAmount_num"
            aggfunc = "sum" 

        else:
            value_col = "wishedCount"
            aggfunc = "sum"

        # -----------------------------
        # PIVOT TABLE
        # -----------------------------
        heatmap = df_filtrado.pivot_table(
            index="pet_type",
            columns="category",
            values=value_col,
            aggfunc=aggfunc,
            fill_value=0
        )
        if normalize:
            heatmap = heatmap.div(heatmap.sum(axis=1), axis=0) * 100

        fig = px.imshow(
            heatmap,
            text_auto=".1f",  
            aspect="auto",
            color_continuous_scale="Blues"
        )
        
        fig.update_layout(
            title=f"Heatmap: Pet vs Categoria ({metric})",
            xaxis_title="Categoria do Produto",
            yaxis_title="Tipo de Pet",
            title_x=0.26,
            hoverlabel=dict(
                bgcolor="#1e1e1e",
                font_color="white",
                font_size=13,
                align="left"
            )
        )
        if normalize:
            fig.update_traces(texttemplate="%{z:.1f}%")
    
        fig.update_traces(
         hovertemplate=
            "Pet: %{y}<br>" +
            "Categoria: %{x}<br>" +
            "Valor: %{z}<br>" +
            "<extra></extra>"
        )
        st.plotly_chart(fig, use_container_width=True, key="heatmap_principal")

media_avaliacao = df_filtrado["averageStar"].mean()
media_avaliacao_formatada = f"{media_avaliacao:.2f}"

# -----------------------------
# INSIGHTS AUTOMÁTICOS
# -----------------------------
col1, col2 = st.columns([1, 2])

with col1:
    with st.container(border=True):
            st.subheader("🧠 Insights automáticos")

            if not heatmap.empty:
                top_pet = heatmap.sum(axis=1).idxmax()
                top_category = heatmap.sum(axis=0).idxmax()

                st.write(f"🐾 O tipo de pet com maior volume geral é: **{top_pet}**")
                st.write(f"📦 A categoria mais forte no geral é: **{top_category}**")

                # Insight cruzado
                max_cell = heatmap.stack().idxmax()
                st.write(f"🔥 Maior concentração: **{max_cell[0]} → {max_cell[1]}**")   

    # CARD (logo abaixo dos insights)
    st.markdown(f"""  
    <div class="kpi-card bg-red">
        <div class="kpi-icon">⭐</div>
        <div class="kpi-info">
            <div class="kpi-value">{media_avaliacao_formatada}</div>
            <div class="kpi-label">Média de Avaliação</div>
            <div class="kpi-change-up">Qualidade geral dos produtos</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        grafico.avaliacao_produto(df_filtrado, categoria_grafico)
import plotly.express as px
import streamlit as st
import pandas as pd

cores_escolhidas = ["#3967BC", "#DD2D4A", "#FFD700", "#985BC1", "#50c5dd",
    "#77DD77", "#FF6961", "#FFD700", "#20B2AA", "#C71585"] #DE9B2F #20B2AA


def avaliacao_produto(df, categoria): #BARRA EM PÉ - avaliação dos produtos - Produto

    if "Todos" in categoria:
        filtro = df
    else:
        filtro = df[
            df["category"].isin(categoria)
        ]

    def faixa_nota(nota):
        if nota >= 4.5:
            return "Excelente"
        elif nota >= 4:
            return "Boa"
        elif nota >= 3:
            return "Média"
        else:
            return "Ruim"

    filtro["faixa"] = filtro["averageStar"].apply(faixa_nota)

    legenda_map = {
        "Excelente": "Excelente (4,5 - 5,0)",
        "Boa": "Boa (4,0 - 4,49)",
        "Média": "Média (3,0 - 3,99)",
        "Ruim": "Ruim (0 - 2,99)"
    }

    filtro["faixa_legenda"] = filtro["faixa"].map(legenda_map)

    contagem = (
        filtro.groupby(["faixa", "faixa_legenda"])
        .size()
        .reset_index(name="count")
    )

    ordem = ["Excelente", "Boa", "Média", "Ruim"]

    contagem["faixa"] = pd.Categorical(
        contagem["faixa"],
        categories=ordem,
        ordered=True
    )

    contagem = contagem.sort_values("faixa")

    fig = px.bar(
        contagem,
        x="faixa",              
        y="count",
        color="faixa_legenda",  
        text="count",
        color_discrete_sequence=[
            "#1f77b4",
            "#4dabf7",
            "#ffa94d",
            "#ff6b6b"
        ]
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate=
        "<b>%{label}</b><br>" +
        "Quantidade: %{value}<br>" +
        "<extra></extra>",
    )
    fig.update_layout(
        title="Distribuição de Avaliações",
        xaxis_title="Avaliação",
        yaxis_title="Quantidade",
        #paper_bgcolor="white",
        #plot_bgcolor="white",
        legend_title="Faixa de avaliação",
        hoverlabel=dict(
            bgcolor="#1e1e1e",
            font_color="white",
            font_size=13,
            align="left"
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    
def estoque_categoria(df, categoria): # Donut - estoque por tipo de categoria do produto- Home

    if "Todos" in categoria:
        filtro = df
    else:
        filtro = df[
            df["category"].isin(categoria)
        ]

    # Agrupa os dados
    dados = (
        filtro.groupby("category")["quantity"]
        .sum()
        .reset_index()
    )

    # Total
    total = dados["quantity"].sum()

    # Labels com porcentagem
    dados["label"] = (
        dados["category"] + " - " +
        ((dados["quantity"] / total) * 100)
        .round(1)
        .astype(str) + "%"
    )

    fig = px.pie(
        dados,
        names="label",
        values="quantity",
        hole=0.6,
        color_discrete_sequence= cores_escolhidas
    )

    fig.update_traces(
        textinfo="none", # Remove textos internos no grafico
        hovertemplate=
        "<b>%{label}</b><br>" +
        "Quantidade: %{value}<br>" +
        "<extra></extra>",

    )

    fig.update_layout(
        title="Distribuição de Estoque por Categoria",

        height=300,
        width=300,

        legend=dict(
            orientation="v",
            y=0.5,
            yanchor="middle",
            x=-0.3,
            xanchor="left",
            font=dict(size=13)
        ),

        margin=dict(t=40,b=20,l=120,r=20),
        
        hoverlabel=dict(
            bgcolor="#1e1e1e",
            font_color="white",
            font_size=13,
            align="left"
        )
    )

    st.plotly_chart(fig, use_container_width=True)     # Exibe no Streamlit

def estoque_pet(df, categoria): # Donut - estoque por tipo de pet - Home
    
    if "Todos" in categoria:
        filtro = df
    else:
        filtro = df[
            df["category"].isin(categoria)
        ]
    # Agrupa os dados
    dados = (
        filtro.groupby("pet_type")["quantity"]
        .sum()
        .reset_index()
    )

    # Total
    total = dados["quantity"].sum()

    # Labels com porcentagem
    dados["label"] = (
        dados["pet_type"] + " - " +
        ((dados["quantity"] / total) * 100)
        .round(1)
        .astype(str) + "%"
    )

    # Cria gráfico donut
    fig = px.pie(
        dados,
        names="label",
        values="quantity",
        hole=0.6,
        color_discrete_sequence= cores_escolhidas
  
    )

    fig.update_traces(
        textinfo="none", # Remove textos internos no grafico
        hovertemplate=
        "<b>%{label}</b><br>" +
        "Quantidade: %{value}<br>"
        "<extra></extra>",

    )

    # Layout
    fig.update_layout(
        title="Distribuição de Estoque por Pet",

        height=300,
        width=300,

        legend=dict(
            orientation="v",
            y=0.5,
            yanchor="middle",
            x=-0.3,
            xanchor="left",
            font=dict(size=13)
        ),

        margin=dict(
            t=40,
            b=20,
            l=120,
            r=20
        ),
        
        hoverlabel=dict(
            bgcolor="#1e1e1e",
            font_color="white",
            font_size=13,
            align="left"
        )
    )
    st.plotly_chart(fig, use_container_width=True)

def venda_categoria_pet(df,categoria, pet): #barra com Categoria e o pet - Home
    if "Todos" in categoria:
        filtro = df
    else:
        filtro = df[
            df["category"].isin(categoria)
        ]
    
    if "Todos" not in pet:

        filtro = filtro[
            filtro["pet_type"].isin(pet)
        ]
    
    # agrupamento
    cal_venda_categoria = (
        filtro.groupby(["category", "pet_type"])["tradeAmount_num"].sum().reset_index()
    )

    # total geral
    total_geral = cal_venda_categoria["tradeAmount_num"].sum()

    # total por categoria
    cal_venda_categoria["total_categoria"] = (
        cal_venda_categoria.groupby("category")["tradeAmount_num"].transform("sum")
    )

    # % do pet dentro da categoria
    cal_venda_categoria["perc_dentro_categoria"] = (
        cal_venda_categoria["tradeAmount_num"]/ cal_venda_categoria["total_categoria"]
    ) * 100

    # % da categoria no geral
    cal_venda_categoria["perc_categoria_geral"] = (
        cal_venda_categoria["total_categoria"]/ total_geral
    ) * 100

    # valores formatados
    cal_venda_categoria["total_categoria_formatado"] = (
        cal_venda_categoria["total_categoria"].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    )

    cal_venda_categoria["vendas_pet_formatado"] = (
        cal_venda_categoria["tradeAmount_num"].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    )

    # gráfico
    fig = px.bar(
        cal_venda_categoria,
        x="category",
        y="tradeAmount_num",
        color="pet_type",
        barmode="relative",
        custom_data=[
            "perc_dentro_categoria",
            "perc_categoria_geral",
            "total_categoria_formatado",
            "vendas_pet_formatado"
        ],
        title="Vendas por Categoria e Tipo de Pet",
        color_discrete_sequence=cores_escolhidas
    )

    # hover
    fig.update_traces(
        hovertemplate=
            "Categoria: %{x}<br>"
            "Pet: %{fullData.name}<br>"
            "Produtos vendidos (pet): %{customdata[3]} (%{customdata[0]:.1f}%)<br>"
            "Total categoria: %{customdata[2]} (%{customdata[1]:.1f}%)<br>"
            "<extra></extra>"
        )

    fig.update_layout(
        height=640,
        xaxis_title="Categoria",
        yaxis_title="Total vendido",

        title=dict(
            text="Vendas por Categoria e Tipo de Pet",
            y=0.985, yanchor="top",          # abaixa o título (0.5 = meio, 1.0 = topo)
            x=0.5,xanchor="right",
        ),

        legend_title=None,

        legend=dict(
            orientation="h",
            y=-0.3, yanchor="bottom",
            x=0.5, xanchor="center", 
            font=dict(size=13)
        ),
        
        hoverlabel=dict(
            bgcolor="#1e1e1e",
            font_color="white",
            font_size=13,
            align="left"
        )
    
    )
    st.plotly_chart(fig, use_container_width=True)

def interesse_venda(df, categoria): # Distribuição com interesse/desejado e vendas- Home
    if "Todos" in categoria:
        filtro = df
    else:
        filtro = df[
            df["category"].isin(categoria)
        ]

   # formatação BR
    filtro["Produtos vendidos"] = (
        filtro["tradeAmount_num"]
        .apply(lambda x: f"{x:,.0f}".replace(",", "."))
    )

    filtro["Interesse"] = (
        filtro["wishedCount"]
        .apply(lambda x: f"{x:,.0f}".replace(",", "."))
    )

    fig = px.scatter(
        filtro,

        x="wishedCount",
        y="tradeAmount_num",

        #size="tradeAmount_num",
        color="category",

        hover_name="title_curto",

        custom_data=[
            "Produtos vendidos",
            "Interesse",
            "pet_type", 
            "category"
        ],

        color_discrete_sequence=cores_escolhidas,

        title="Interesse vs Quantidade Vendida"
    )

    fig.update_xaxes(type="log")
    fig.update_yaxes(type="log")

    fig.update_traces(
        hovertemplate=
            "<b>%{hovertext}</b><br><br>"
            "Categoria: %{customdata[3]}<br>"
            "Pet: %{customdata[2]}<br>"
            "Produtos vendidos: %{customdata[0]}<br>"
            "Interesse: %{customdata[1]}<br>"
            "<extra></extra>"
    )

    fig.update_layout(
        barmode="stack",
        legend_title=None,
        title=dict(
        y=0.96,          # sobe o título (0.5 é meio, 1.0 é topo)
        x=0.5,           # centraliza horizontalmente
        xanchor="center",
        yanchor="top"),
        margin=dict(t=40),
        xaxis_title="Interesse",
        yaxis_title="Quantidade Vendida",
        legend=dict(
            orientation="h",
            y=-0.4,
            yanchor="bottom",
            x=0,
            xanchor="left", 
            font=dict(size=13)
        ),
        hoverlabel=dict(
            bgcolor="#1e1e1e",
            font_color="white",
            font_size=13,
            align="left"
        )
    
    )
    st.plotly_chart(fig, use_container_width=True)

def avaliacao_venda(df, categoria): # Distribuição com avaliação e vendas- Home
    if "Todos" in categoria:
        filtro = df
    else:
        filtro = df[
            df["category"].isin(categoria)
        ]

    filtro["Produtos vendidos"] = (
        filtro["tradeAmount_num"]
        .apply(lambda x: f"{x:,.0f}".replace(",", "."))
    )

    filtro["avaliacao"] = (
        filtro["averageStar"]
        .apply(lambda x: f"{x:,.1f}".replace(",", "."))
    )

    fig = px.scatter(
        filtro,
        x="averageStar",       # eixo X = avaliação
        y="tradeAmount_num",         # eixo Y = quant de vendas
        #size="tradeAmount_num",      # bolha maior = mais vendas
        color="category",
        color_discrete_sequence= cores_escolhidas,    # cor por produto
        title="Avaliação vs Quantidade Vendida",
        hover_name="title_curto",
        custom_data=[
            "Produtos vendidos",
            "avaliacao",
            "pet_type", 
            "category"
        ],
    )

    fig.update_xaxes(type="log")
    fig.update_yaxes(type="log")

    fig.update_traces(
        hovertemplate=
            "<b>%{hovertext}</b><br><br>"
            "Categoria: %{customdata[3]}<br>"
            "Pet: %{customdata[2]}<br>"
            "Produtos vendidos: %{customdata[0]}<br>"
            "Avaliação: %{customdata[1]}<br>"
            "<extra></extra>"
    )
    fig.update_layout(
        barmode="stack",
        legend_title=None,
        title=dict(
        y=0.96,          # sobe o título (0.5 é meio, 1.0 é topo)
        x=0.5,           # centraliza horizontalmente
        xanchor="center",
        yanchor="top"),
        margin=dict(t=40),
        xaxis_title="Avaliação",
        yaxis_title="Quantidade Vendida",
        legend=dict(
            orientation="h",
            y=-0.4,
            yanchor="bottom",
            x=0,
            xanchor="left", 
            font=dict(size=13)
        ),
        hoverlabel=dict(
            bgcolor="#1e1e1e",
            font_color="white",
            font_size=13,
            align="left"
        )
    )

    st.plotly_chart(fig, use_container_width=True)
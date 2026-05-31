import streamlit as st
import pandas as pd

# -------------------------------------------------------------------------------
def interface():

    st.set_page_config(page_title="Dashboard Pet Shop", layout="wide")

    st.markdown("""
    <style>

    /* fundo da sidebar */
    section[data-testid="stSidebar"] {
        background-color: #3967BC;
    }

    /* remove espaço topo */
    section[data-testid="stSidebar"] > div {
        padding-top: 0px;
    }

    /* logo branca */
    section[data-testid="stSidebar"] img {
        margin: -90px 0 -50px -22px;
        filter: brightness(0) invert(1);
    }

    /* texto branco */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* =========================================
    BORDA BRANCA NOS EXPANDERS
    ========================================= */
    section[data-testid="stSidebar"] div[data-testid="stExpander"] {
        border: 1px solid white !important;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    section[data-testid="stSidebar"] details > div {
        border-top: 1px solid white !important;
    }

    /* =========================================
    REMOVE FUNDO BRANCO
    ========================================= */

    section[data-testid="stSidebar"] label[data-baseweb="checkbox"],
    section[data-testid="stSidebar"] label[data-baseweb="checkbox"]:hover,
    section[data-testid="stSidebar"] label[data-baseweb="checkbox"]:active,
    section[data-testid="stSidebar"] label[data-baseweb="checkbox"]:focus,
    section[data-testid="stSidebar"] label[data-baseweb="checkbox"]:focus-visible {
        background-color: transparent !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="checkbox"] {
        background-color: transparent !important;
    }

    /* expander */
    section[data-testid="stSidebar"] details,
    section[data-testid="stSidebar"] details[open],
    section[data-testid="stSidebar"] summary,
    section[data-testid="stSidebar"] summary:hover,
    section[data-testid="stSidebar"] summary:active,
    section[data-testid="stSidebar"] summary:focus,
    section[data-testid="stSidebar"] summary:focus-visible {
        background-color: transparent !important;
    }

    section[data-testid="stSidebar"] .streamlit-expanderContent {
        background-color: transparent !important;
    }

    /* remove foco branco */
    section[data-testid="stSidebar"] *:focus,
    section[data-testid="stSidebar"] *:focus-visible,
    section[data-testid="stSidebar"] *:active {
        background-color: transparent !important;
        outline: none !important;
        box-shadow: none !important;
    }

    section[data-testid="stSidebar"] * {
        -webkit-tap-highlight-color: transparent !important;
    }

    /* =========================================
    TEXTO MUDA DE COR NO HOVER
    ========================================= */
    section[data-testid="stSidebar"] label[data-baseweb="checkbox"]:hover,
    section[data-testid="stSidebar"] label[data-baseweb="checkbox"]:hover span {
        color: #3967BC !important;
    }

    /* =========================================
    BOTÃO LIMPAR FILTROS
    ========================================= */

    /* base */
    section[data-testid="stSidebar"] div.stButton > button {
        background-color: #3967BC !important;
        color: white !important;
        border: 1px solid white !important;
    }

    /* hover + clique + foco */
    section[data-testid="stSidebar"] div.stButton > button:hover,
    section[data-testid="stSidebar"] div.stButton > button:active,
    section[data-testid="stSidebar"] div.stButton > button:focus,
    section[data-testid="stSidebar"] div.stButton > button:focus-visible {
        background-color: #CBEEF3 !important;
        color: #3967BC !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /*(texto interno) */
    section[data-testid="stSidebar"] div.stButton > button:hover *,
    section[data-testid="stSidebar"] div.stButton > button:active *,
    section[data-testid="stSidebar"] div.stButton > button:focus *,
    section[data-testid="stSidebar"] div.stButton > button:focus-visible * {
        color: #3967BC !important;
    }

    .block-container {
        padding-top: 2rem;
    }

    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------------
    st.title("🐾 Dashboard de Vendas - PetSmart")
    st.sidebar.image("imagens/petSmartLogo.svg", width=250)

    @st.cache_data
    def carregar():
        return pd.read_csv("data/pet_supplies_correto.csv")

    df = carregar()

    st.sidebar.title("Filtros")

    # -------------------------------
    # CONFIG
    # -------------------------------
    categorias = {
        "brinquedos": "Brinquedos",
        "alimentacao": "Alimentação",
        "acessorios": "Acessórios",
        "conforto": "Conforto",
        "higiene": "Higiene",
        "outros": "Outros",
    }

    pets_lista = sorted(df["pet_type"].dropna().unique())

    avaliacoes = {
        "av_0_1": (0,1),
        "av_1_2": (1,2),
        "av_2_3": (2,3),
        "av_3_4": (3,4),
        "av_4_5": (4,5),
    }

    # -------------------------------
    # INIT
    # -------------------------------
    def init(keys):
        for k in keys:
            st.session_state.setdefault(k, False)

    init(["todas"] + list(categorias))
    init(["todas_pets"] + [f"pet_{p}" for p in pets_lista])
    init(["todas_avaliacoes"] + list(avaliacoes))

    # -------------------------------
    # CALLBACKS
    # -------------------------------
    def marcar_todos(master, keys):
        for k in keys:
            st.session_state[k] = st.session_state[master]

    def atualizar_master(master, keys):
        st.session_state[master] = all(st.session_state[k] for k in keys)

    # -------------------------------
    # UI
    # -------------------------------
    with st.sidebar.expander("Categorias"):
        st.checkbox("Selecionar tudo", key="todas",
                    on_change=lambda: marcar_todos("todas", categorias.keys()))

        for k, nome in categorias.items():
            st.checkbox(nome, key=k,
                        on_change=lambda: atualizar_master("todas", categorias.keys()))

    with st.sidebar.expander("Pets"):
        st.checkbox("Selecionar tudo", key="todas_pets",
                    on_change=lambda: marcar_todos("todas_pets", [f"pet_{p}" for p in pets_lista]))

        for pet in pets_lista:
            st.checkbox(pet, key=f"pet_{pet}",
                        on_change=lambda: atualizar_master("todas_pets", [f"pet_{p}" for p in pets_lista]))

    with st.sidebar.expander("Avaliações"):
        st.checkbox("Selecionar tudo", key="todas_avaliacoes",
                    on_change=lambda: marcar_todos("todas_avaliacoes", avaliacoes.keys()))

        for k, (a,b) in avaliacoes.items():
            st.checkbox(f"{a} a {b}⭐", key=k,
                        on_change=lambda: atualizar_master("todas_avaliacoes", avaliacoes.keys()))

    # -------------------------------
    # LIMPAR
    # -------------------------------
    def limpar():
        for k in st.session_state.keys():
            st.session_state[k] = False

    st.sidebar.button("Limpar Filtros", on_click=limpar)

    # -------------------------------
    # FILTRO
    # -------------------------------
    df_filtrado = df.copy()

    cats_sel = [nome for k, nome in categorias.items() if st.session_state[k]]
    if cats_sel:
        df_filtrado = df_filtrado[df_filtrado["category"].isin(cats_sel)]

    pets_sel = [p for p in pets_lista if st.session_state[f"pet_{p}"]]
    if pets_sel:
        df_filtrado = df_filtrado[df_filtrado["pet_type"].isin(pets_sel)]

    faixas = [v for k,v in avaliacoes.items() if st.session_state[k]]

    if "averageStar" in df_filtrado.columns and faixas:
        cond = False
        for a,b in faixas:
            cond |= df_filtrado["averageStar"].between(a,b)
        df_filtrado = df_filtrado[cond]

    return df_filtrado, cats_sel, pets_sel
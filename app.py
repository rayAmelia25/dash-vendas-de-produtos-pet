import streamlit as st

st.set_page_config(page_title="Dashboard Pets", layout="wide")
import streamlit as st

st.set_page_config(
    page_title="Dashboard Pets",
    layout="wide"
)

pages = {
    "": [

        st.Page(
            "pages/home.py",
            title="Home"
        ),

        st.Page(
            "pages/produto.py",
            title="Produto"
        ),
    ]

}

pg = st.navigation(
    pages,
    position="top"
)

pg.run()
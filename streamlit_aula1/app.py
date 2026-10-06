import streamlit as st
import pandas as pd

nome = "Pedro Henrique"
idade = 20

st.title("Meu primeiro dash")
st.subheader(nome)


st.write("Olá, mundo")


st.write(f"Meu nome é {nome} e tenho {idade} anos.")


df = pd.DataFrame({
    'Matéria': ['Português', 'Matemática', 'Python', 'Frame'],
    'Nota': [5, 9, 7, 10]
})


st.write(df)

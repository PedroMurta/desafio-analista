from flask import Flask, render_template
import streamlit as st
import requests

app = Flask(__name__)

# Define a rota inicial
@app.route("/")
def index():
    # Utiliza o pacote requests para fazer a requisição do Streamlit
    response = requests.get("http://localhost:8501/")
    # Retorna o conteúdo do Streamlit como uma string
    return response.text

# Define a rota para renderizar o Streamlit
@app.route("/streamlit")
def streamlit():
    # Utiliza o pacote streamlit para renderizar a página desejada
    st.set_page_config(page_title="Desafio Analista", page_icon=":pencil:", layout="wide")
    from streamlit_app import main
    main()

if __name__ == "__main__":
    app.run(debug=True, port=8501)

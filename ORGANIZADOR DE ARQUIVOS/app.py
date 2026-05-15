import os
import shutil
import time
import streamlit as st
from tkinter import Tk
from tkinter.filedialog import askdirectory

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Organizador de Arquivos",
    page_icon="📂",
    layout="centered"
)

# TÍTULO
st.title("📂 Organizador Automático de Arquivos")

st.write("Escolha uma pasta e organize automaticamente seus arquivos.")

# SESSION STATE
if "pasta" not in st.session_state:
    st.session_state.pasta = ""

# FUNÇÃO PARA ESCOLHER PASTA
def escolher_pasta():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    pasta = askdirectory()

    root.destroy()

    return pasta

# BOTÃO ESCOLHER PASTA
if st.button("📁 Escolher Pasta"):
    pasta_escolhida = escolher_pasta()

    if pasta_escolhida:
        st.session_state.pasta = pasta_escolhida

# MOSTRAR PASTA
if st.session_state.pasta:
    st.success(f"Pasta selecionada: {st.session_state.pasta}")

# CATEGORIAS
categorias = {
    "Imagens": [".png", ".jpg", ".jpeg", ".gif"],
    "Videos": [".mp4", ".mov", ".avi"],
    "PDFs": [".pdf"],
    "Planilhas": [".xlsx", ".csv"],
    "Musicas": [".mp3"],
    "Documentos": [".docx", ".txt"],
    "Compactados": [".zip", ".rar", ".7z"],
    "Programas": [".exe", ".msi"],
    "Python": [".py", ".ipynb"]
}

# BOTÃO ORGANIZAR
if st.button("🚀 Organizar Arquivos"):

    pasta = st.session_state.pasta

    if not pasta:
        st.error("Escolha uma pasta primeiro.")

    else:

        arquivos = os.listdir(pasta)

        arquivos_validos = []

        # FILTRA APENAS ARQUIVOS
        for arquivo in arquivos:

            caminho_arquivo = os.path.join(pasta, arquivo)

            if os.path.isfile(caminho_arquivo):
                arquivos_validos.append(arquivo)

        total_arquivos = len(arquivos_validos)

        if total_arquivos == 0:
            st.warning("Nenhum arquivo encontrado.")

        else:

            barra = st.progress(0)

            status = st.empty()

            logs = st.empty()

            log_texto = ""

            for i, arquivo in enumerate(arquivos_validos):

                caminho_arquivo = os.path.join(pasta, arquivo)

                extensao = os.path.splitext(arquivo)[1].lower()

                arquivo_movido = False

                for categoria, extensoes in categorias.items():

                    if extensao in extensoes:

                        pasta_categoria = os.path.join(pasta, categoria)

                        os.makedirs(pasta_categoria, exist_ok=True)

                        destino = os.path.join(pasta_categoria, arquivo)

                        shutil.move(caminho_arquivo, destino)

                        log_texto += f"✔ {arquivo} → {categoria}\n"

                        logs.text(log_texto)

                        arquivo_movido = True

                        break

                if not arquivo_movido:

                    log_texto += f"⚠ {arquivo} → Sem categoria\n"

                    logs.text(log_texto)

                progresso = int(((i + 1) / total_arquivos) * 100)

                barra.progress(progresso)

                status.write(f"Progresso: {progresso}%")

                time.sleep(0.2)

            st.success("✅ Organização concluída com sucesso!")
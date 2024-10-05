import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Validação de relatórios de sentença gerados por LLM", page_icon=":robot_face:", layout="wide")

# Título da aplicação
st.title('Validação de relatórios de sentença gerados por LLM')

with st.expander("Instruções"):
    st.write('''
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    ''')

def inicializar_variaveis():
    st.session_state.linha = 0
    # st.session_state.num_processo = df["num_processo"]
    st.session_state.num_processo = []
    st.session_state.gpt4ov1_a = []
    st.session_state.gpt4ov1_v = []
    st.session_state.gpt4ov1_f = []
    st.session_state.gpt4ominiv1_a = []
    st.session_state.gpt4ominiv1_v = []
    st.session_state.gpt4ominiv1_f = []
    st.session_state.llamav1_a = []
    st.session_state.llamav1_v = []
    st.session_state.llamav1_f = []
    st.session_state.gpt4ov2_a = []
    st.session_state.gpt4ov2_v = []
    st.session_state.gpt4ov2_f = []
    st.session_state.gpt4ominiv2_a = []
    st.session_state.gpt4ominiv2_v = []
    st.session_state.gpt4ominiv2_f = []
    st.session_state.llamav2_a = []
    st.session_state.llamav2_v = []
    st.session_state.llamav2_f = []

def mostrar_proxima_linha():
    st.session_state.num_processo.append(df["num_processo"][st.session_state.linha])
    st.session_state.gpt4ov1_a.append(gpt4ov1_a)
    st.session_state.gpt4ov1_v.append(gpt4ov1_v)
    st.session_state.gpt4ov1_f.append(gpt4ov1_f)

    st.session_state.linha += 1
    # st.write("linha = " + str(st.session_state.linha) + " " + str(datetime.now().strftime("%H:%M:%S:%f")))

    # if st.session_state.linha >= len(df):
        # st.session_state.linha = 0
        # st.write(len(st.session_state.num_processo))
        # st.write(len(st.session_state.gpt4ov1_a))
        # st.write(len(st.session_state.gpt4ov1_v))
        # st.write(len(st.session_state.gpt4ov1_f))
        # inicializar_variaveis()

# Carregar o arquivo Excel
uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx"], on_change=inicializar_variaveis)

if uploaded_file is not None:
    st.write("linha = " + str(st.session_state.linha) + " " + str(datetime.now().strftime("%H:%M:%S:%f")))

    df = pd.read_excel(uploaded_file)

    if st.session_state.linha < len(df):
        # linha = st.session_state.linha
        # st.write("linha < len(df): linha = " + str(linha) + " " + str(datetime.now().strftime("%H:%M:%S:%f")))

        st.header("Relatório de sentença original")

        st.subheader("Processo: " + df["num_processo"][st.session_state.linha])

        with st.container(height=300):
            st.markdown(df["reference"][st.session_state.linha])
            # st.markdown('<span style="font-size: 12px;">' + df["reference"][st.session_state.linha] + '</span>', unsafe_allow_html=True)

        st.header("Relatórios de sentença gerados por LLM")

        # col1, col2 = st.columns([3, 1], vertical_alignment="top")
        col1, col2 = st.columns([3, 1])

        with col1:
            with st.container(height=300):
                st.markdown(df["gpt-4o-v1"][st.session_state.linha])
                # st.markdown('<span style="font-size: 12px;">'+df["gpt-4o-v1"][st.session_state.linha]+'</span>', unsafe_allow_html=True)

        with col2:
            st.write("a")
            gpt4ov1_a = st.radio("Acurácia?", ("Sim", "Não"), key="gpt4ov1_ac")
            gpt4ov1_v = st.radio("Verdade?", ("Sim", "Não"), key="gpt4ov1_ve")
            gpt4ov1_f = st.radio("Fluência?", ("Sim", "Não"), key="gpt4ov1_fl")

        st.divider()

        col1, col2 = st.columns([3, 1], vertical_alignment="top")

        with col1:
            with st.container(height=300):
                st.markdown(df["gpt-4o-mini-v1"][st.session_state.linha])
                # st.html('<span style="font-size: 12px;">'+df["gpt-4o-mini-v1"][st.session_state.linha]+'</span>')

        with col2:
            st.write("a")
            # acuracia = st.radio("Acurácia?", ("Sim", "Não"), key="gpt4ominiv1_a")
            # verdade = st.radio("Verdade?", ("Sim", "Não"), key="gpt4ominiv1_v")
            # fluencia = st.radio("Fluência?", ("Sim", "Não"), key="gpt4ominiv1_f")

        st.divider()

        col1, col2 = st.columns([3, 1], vertical_alignment="top")

        with col1:
            with st.container(height=300):
                st.markdown(df["gpt-4o-v2"][st.session_state.linha])
                # st.html('<span style="font-size: 12px;">'+df["gpt-4o-v2"][st.session_state.linha]+'</span>')

        with col2:
            st.write("a")
            # acuracia = st.radio("Acurácia?", ("Sim", "Não"), key="gpt4ominiv1_a")
            # verdade = st.radio("Verdade?", ("Sim", "Não"), key="gpt4ominiv1_v")
            # fluencia = st.radio("Fluência?", ("Sim", "Não"), key="gpt4ominiv1_f")

        st.divider()

        col1, col2 = st.columns([3, 1], vertical_alignment="top")

        with col1:
            with st.container(height=300):
                st.markdown(df["gpt-4o-mini-v2"][st.session_state.linha])
                # st.html('<span style="font-size: 12px;">'+df["gpt-4o-mini-v2"][st.session_state.linha]+'</span>')

        with col2:
            st.write("a")
            # acuracia = st.radio("Acurácia?", ("Sim", "Não"), key="gpt4ominiv1_a")
            # verdade = st.radio("Verdade?", ("Sim", "Não"), key="gpt4ominiv1_v")
            # fluencia = st.radio("Fluência?", ("Sim", "Não"), key="gpt4ominiv1_f")

        # llama-v1
        # llama-v2

        # # genre = st.radio(
        # #     "What's your favorite movie genre",
        # #     [":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"],
        # #     captions=[
        # #         "Laugh out loud.",
        # #         "Get the popcorn.",
        # #         "Never stop learning.",
        # #     ],
        # # )
        #

        # col_a, col_v, col_f = st.columns(3)
        #
        # # Adicionar um botão de rádio em cada coluna
        # with col_a:
        #     acuracia = st.radio("Acurácia?", ("Sim", "Não"), key="acuracia")
        #
        # with col_v:
        #     verdade = st.radio("Verdade?", ("Sim", "Não"), key="verdade")
        #
        # with col_f:
        #     fluencia = st.radio("Fluência?", ("Sim", "Não"), key="fluencia")

        st.button('Próximo processo', on_click=mostrar_proxima_linha, key='botao_mostrar_proxima_linha')
        # if st.button('Próximo processo'):
        #     mostrar_proxima_linha()

    else:
        st.write(len(st.session_state.num_processo))
        st.write(len(st.session_state.gpt4ov1_a))
        st.write(len(st.session_state.gpt4ov1_v))
        st.write(len(st.session_state.gpt4ov1_f))

        respostas = {
            "num_processo": st.session_state.num_processo,
            "gpt4ov1_a": st.session_state.gpt4ov1_a,
            "gpt4ov1_v": st.session_state.gpt4ov1_v,
            "gpt4ov1_f": st.session_state.gpt4ov1_f,
            # "gpt4ominiv1_a": gpt4ominiv1_a,
            # "gpt4ominiv1_v": gpt4ominiv1_v,
            # "gpt4ominiv1_f": gpt4ominiv1_f,
            # "llamav1_a": llamav1_a,
            # "llamav1_v": llamav1_v,
            # "llamav1_f": llamav1_f,
            # "gpt4ov2_a": gpt4ov2_a,
            # "gpt4ov2_v": gpt4ov2_v,
            # "gpt4ov2_f": gpt4ov2_f,
            # "gpt4ominiv2_a": gpt4ominiv2_a,
            # "gpt4ominiv2_v": gpt4ominiv2_v,
            # "gpt4ominiv2_f": gpt4ominiv2_f,
            # "llamav2_a": llamav2_a,
            # "llamav2_v": llamav2_v,
            # "llamav2_f": llamav2_f,
        }

        df_respostas = pd.DataFrame(respostas)
        df_respostas.to_excel("Respostas.xlsx", index=False)

        # Ler o arquivo Excel gerado
        with open("Respostas.xlsx", "rb") as file:
            st.download_button(
                label="Salvar respostas",
                data=file,
                file_name="Respostas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

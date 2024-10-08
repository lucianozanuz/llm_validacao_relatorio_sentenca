import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Validação de relatórios de sentença gerados por LLM", page_icon=":classical_building:", layout="wide")

# Título da aplicação
st.title('Validação de relatórios de sentença gerados por LLM')

with st.expander("Instruções para avaliação dos relatórios de sentença gerados por LLM"):
    st.write('''
        A metodologia de avaliação deste trabalho foi baseada no **MQM Framework** (https://themqm.org/).
        
        Avalie com nota mais baixa se o texto contém problemas graves no critério, com nota mais alta se os problemas forem leves e com nota máxima se considerar que não há problemas no critério.

        Critérios avaliados (considerar TEXTO_ALVO como o relatório de sentença gerado por LLM e TEXTO_REFERENCIA como o relatório de sentença escrito pelo juiz):
        - **Acurácia**: Refere-se ao nível em que o conteúdo do TEXTO_ALVO representa o conteúdo do TEXTO_REFERENCIA, considerando a terminologia (se o TEXTO_ALVO contém termos legais obrigatórios), a omissão e a inclusão de termos importantes ou obrigatórios.
          - Exemplo de problemas graves: TEXTO_ALVO não se refere ao mesmo processo judicial relatado no TEXTO_REFERENCIA;
          - Exemplo de problemas leves: TEXTO_ALVO se refere ao mesmo processo judicial relatado no TEXTO_REFERENCIA, mas, omite termos legais obrigatórios ou inclui termos inadequados para um relatório de sentença;
        - **Verdade**: Refere-se a se o TEXTO_ALVO contém os requisitos do Código do Processo Civil (nomes das partes, a identificação do caso, os pedidos da inicial e da contestação e registro das principais ocorrências do processo)
        - **Fluência**: Refere-se ao estilo (TEXTO_ALVO deve ser formal, mas seguir os princípios da linguagem simples), ortografia, gramática, violações locais (o formato de datas, valores, números, telefones e endereços segue o padrão local do Brasil) e interrupções, como divisão em seções ou subtítulos.
    ''')


def inicializar_variaveis():
    st.session_state.linha = 0
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
    if gpt4ov1_ac is None or gpt4ov1_ve is None or gpt4ov1_fl is None or \
        gpt4ominiv1_ac is None or gpt4ominiv1_ve is None or gpt4ominiv1_fl is None or \
        gpt4ov2_ac is None or gpt4ov2_ve is None or gpt4ov2_fl is None or \
        gpt4ominiv2_ac is None or gpt4ominiv2_ve is None or gpt4ominiv2_fl is None:
        st.error("Informe todas as avaliações")
    else:
        st.session_state.num_processo.append(df["num_processo"][st.session_state.linha])
        st.session_state.gpt4ov1_a.append(gpt4ov1_ac + 1)
        st.session_state.gpt4ov1_v.append(gpt4ov1_ve + 1)
        st.session_state.gpt4ov1_f.append(gpt4ov1_fl + 1)
        st.session_state.gpt4ominiv1_a.append(gpt4ominiv1_ac + 1)
        st.session_state.gpt4ominiv1_v.append(gpt4ominiv1_ve + 1)
        st.session_state.gpt4ominiv1_f.append(gpt4ominiv1_fl + 1)
        # st.session_state.llamav1_a.append()
        # st.session_state.llamav1_v.append()
        # st.session_state.llamav1_f.append()
        st.session_state.gpt4ov2_a.append(gpt4ov2_ac + 1)
        st.session_state.gpt4ov2_v.append(gpt4ov2_ve + 1)
        st.session_state.gpt4ov2_f.append(gpt4ov2_fl + 1)
        st.session_state.gpt4ominiv2_a.append(gpt4ominiv2_ac + 1)
        st.session_state.gpt4ominiv2_v.append(gpt4ominiv2_ve + 1)
        st.session_state.gpt4ominiv2_f.append(gpt4ominiv2_fl + 1)
        # st.session_state.llamav2_a.append()
        # st.session_state.llamav2_v.append()
        # st.session_state.llamav2_f.append()
        st.session_state.linha += 1


# Carregar o arquivo Excel
uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx"], on_change=inicializar_variaveis)

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    if st.session_state.linha < len(df):
        progress = (st.session_state.linha + 1) / len(df)
        st.progress(progress, str((st.session_state.linha + 1)) + " de " + str(len(df)) + " processos")

        st.subheader("Relatório de sentença original")
        with st.container(height=300):
            st.markdown(df["reference"][st.session_state.linha])

        txt_acuracia = "Acurácia (comparação com o relatório do juiz):"
        txt_verdade = "Verdade (requisitos do CPC):"
        txt_fluencia = "Fluência (estilo, ortografia, gramática):"

        st.subheader("Relatórios gerados por LLM")

        st.write("##### Relatório de sentença 1")
        col1, col2 = st.columns([3, 1], vertical_alignment="center")

        with col1:
            with st.container(height=300):
                st.markdown(df["gpt-4o-v1"][st.session_state.linha])

        with col2:
            st.write(txt_acuracia)
            gpt4ov1_ac = st.feedback("stars", key="gpt4ov1_ac"+str(st.session_state.linha))
            st.write(txt_verdade)
            gpt4ov1_ve = st.feedback("stars", key="gpt4ov1_ve"+str(st.session_state.linha))
            st.write(txt_fluencia)
            gpt4ov1_fl = st.feedback("stars", key="gpt4ov1_fl"+str(st.session_state.linha))

        st.divider()

        st.write("##### Relatório de sentença 2")
        col1, col2 = st.columns([3, 1], vertical_alignment="center")

        with col1:
            with st.container(height=300):
                st.markdown(df["gpt-4o-mini-v1"][st.session_state.linha])

        with col2:
            st.write(txt_acuracia)
            gpt4ominiv1_ac = st.feedback("stars", key="gpt4ominiv1_ac"+str(st.session_state.linha))
            st.write(txt_verdade)
            gpt4ominiv1_ve = st.feedback("stars", key="gpt4ominiv1_ve"+str(st.session_state.linha))
            st.write(txt_fluencia)
            gpt4ominiv1_fl = st.feedback("stars", key="gpt4ominiv1_fl"+str(st.session_state.linha))

        st.divider()

        st.write("##### Relatório de sentença 3")
        col1, col2 = st.columns([3, 1], vertical_alignment="center")

        with col1:
            with st.container(height=300):
                st.markdown(df["gpt-4o-v2"][st.session_state.linha])

        with col2:
            st.write(txt_acuracia)
            gpt4ov2_ac = st.feedback("stars", key="gpt4ov2_ac"+str(st.session_state.linha))
            st.write(txt_verdade)
            gpt4ov2_ve = st.feedback("stars", key="gpt4ov2_ve"+str(st.session_state.linha))
            st.write(txt_fluencia)
            gpt4ov2_fl = st.feedback("stars", key="gpt4ov2_fl"+str(st.session_state.linha))

        st.divider()

        st.write("##### Relatório de sentença 4")
        col1, col2 = st.columns([3, 1], vertical_alignment="center")

        with col1:
            with st.container(height=300):
                st.markdown(df["gpt-4o-mini-v2"][st.session_state.linha])

        with col2:
            st.write(txt_acuracia)
            gpt4ominiv2_ac = st.feedback("stars", key="gpt4ominiv2_ac"+str(st.session_state.linha))
            st.write(txt_verdade)
            gpt4ominiv2_ve = st.feedback("stars", key="gpt4ominiv2_ve"+str(st.session_state.linha))
            st.write(txt_fluencia)
            gpt4ominiv2_fl = st.feedback("stars", key="gpt4ominiv2_fl"+str(st.session_state.linha))

        st.button('Próximo processo', on_click=mostrar_proxima_linha, key='botao_mostrar_proxima_linha')

    else:
        respostas = {
            "num_processo": st.session_state.num_processo,
            "gpt4ov1_a": st.session_state.gpt4ov1_a,
            "gpt4ov1_v": st.session_state.gpt4ov1_v,
            "gpt4ov1_f": st.session_state.gpt4ov1_f,
            "gpt4ominiv1_a": st.session_state.gpt4ominiv1_a,
            "gpt4ominiv1_v": st.session_state.gpt4ominiv1_v,
            "gpt4ominiv1_f": st.session_state.gpt4ominiv1_f,
            # "llamav1_a": st.session_state.llamav1_a,
            # "llamav1_v": st.session_state.llamav1_v,
            # "llamav1_f": st.session_state.llamav1_f,
            "gpt4ov2_a": st.session_state.gpt4ov2_a,
            "gpt4ov2_v": st.session_state.gpt4ov2_v,
            "gpt4ov2_f": st.session_state.gpt4ov2_f,
            "gpt4ominiv2_a": st.session_state.gpt4ominiv2_a,
            "gpt4ominiv2_v": st.session_state.gpt4ominiv2_v,
            "gpt4ominiv2_f": st.session_state.gpt4ominiv2_f,
            # "llamav2_a": llamav2_a,
            # "llamav2_v": llamav2_v,
            # "llamav2_f": llamav2_f,
        }

        arquivo_retorno = uploaded_file.name.split(".")[0]+"-retorno.xlsx"
        df_respostas = pd.DataFrame(respostas)
        df_respostas.to_excel(arquivo_retorno, index=False)

        # Ler o arquivo Excel gerado
        with open(arquivo_retorno, "rb") as file:
            st.download_button(
                label="Salvar respostas",
                type="primary",
                data=file,
                # file_name=uploaded_file.name.split(".")[0]+"-retorno.xlsx",
                file_name=arquivo_retorno,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

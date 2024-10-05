import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Validação de relatórios de sentença gerados por LLM", page_icon=":robot_face:", layout="wide")

# Título da aplicação
st.title('Validação de relatórios de sentença gerados por LLM')

with st.expander("Instruções"):
    st.write('''
        Considere os seguintes critérios de avaliação baseados no MQM Framework.    
        Acurácia: Problemas relacionados a quão bem o conteúdo do TEXTO_ALVO representa o conteúdo do TEXTO_REFERENCIA, considerando a terminologia (se o TEXTO_ALVO contém termos legais obrigatórios), a omissão e a inclusão de termos importantes ou obrigatórios.  
        Verdade: Problemas relacionados a se o TEXTO_ALVO contém requisitos do Código do Processo Civil (o TEXTO_ALVO deverá conter os nomes das partes, a identificação do caso, com a suma do pedido e da contestação e o registro das principais ocorrências havidas no andamento do processo; o TEXTO_ALVO precisa conter o nomes das partes, o tipo de ação, os pedidos da inicial, os pedidos da contestação e sobre as principais ocorrências; por exemplo, no Procedimento Comum Civil deve conter as audiências e os laudos periciais).  
        Fluência: Problemas ao estilo (o TEXTO_ALVO é formal, mas segue os princípios da linguagem simples), ortografia (o TEXTO_ALVO possui ortografia correta), gramática (o TEXTO_ALVO possui gramática correta), violações locais (o formato de datas, valores, números, telefones e endereços do TEXTO_ALVO segue o padrão local do Brasil).  
        Retorne apenas o resumo da análise da seguinte forma, em formato JSON.  
        Acurácia: 5 se contém problemas graves de Acurácia (Exemplo: TEXTO_ALVO não se refere ao mesmo processo judicial relatado no TEXTO_REFERENCIA); 3 se contém problemas leves de Acurácia (Exemplo: TEXTO_ALVO se refere ao mesmo processo judicial relatado no TEXTO_REFERENCIA, mas, omite termos legais obrigatórios ou inclui termos inadequados para um relatório de sentença); 0 se não contém problemas de Acurácia (Exemplo: TEXTO_ALVO se refere ao mesmo processo judicial relatado no TEXTO_REFERENCIA, não omite termos legais obrigatórios e não inclui termos inadequados para um relatório de sentença).  
        Verdade: 5 se contém problemas graves de Verdade (Exemplo: TEXTO_ALVO não contém o nomes das partes, o tipo de ação e os pedidos da inicial e da contestação); 3 se contém problemas leves de Verdade (Exemplo: TEXTO_ALVO contém o nomes das partes, o tipo de ação e os pedidos da inicial, mas não descreve adequadamente as principais ocorrências como audiências e laudos periciais, se existirem no TEXTO_REFERENCIA); 0 se não contém problemas de Verdade (Exemplo: TEXTO_ALVO contém o nomes das partes, o tipo de ação e os pedidos da inicial, e descreve adequadamente as principais ocorrências como audiências e laudos periciais, se existirem no TEXTO_REFERENCIA).  
        Fluência: 5 se contém problemas graves de Fluência (Exemplo: TEXTO_ALVO contém interrupções, como divisão em seções ou subtítulos); 3 se contém problemas leves de Fluência (Exemplo: TEXTO_ALVO não contém interrupções, como divisão em seções ou subtítulos, mas não segue os princípios da linguagem simples ou possui erros de ortografia ou gramática ou o formato de datas, valores, números, telefones e endereços não segue o padrão local do Brasil); 0 se não contém problemas de Fluência (Exemplo: TEXTO_ALVO não contém interrupções, como divisão em seções ou subtítulos, segue os princípios da linguagem simples e não possui erros de ortografia e gramática e o formato de datas, valores, números, telefones e endereços segue o padrão local do Brasil).      
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
    st.write(gpt4ominiv1_ac)
    st.write(gpt4ominiv1_ve)
    st.write(gpt4ominiv1_fl)

    st.write("antes")
    st.write(st.session_state.gpt4ominiv1_a)

    st.write("gpt4ov1_a="+str(len(st.session_state.gpt4ov1_a)))
    st.write("gpt4ominiv1_a="+str(len(st.session_state.gpt4ominiv1_a)))

    if gpt4ov1_ac is None or gpt4ov1_ve is None or gpt4ov1_fl is None or \
        gpt4ominiv1_ac is None or gpt4ominiv1_ve is None or gpt4ominiv1_fl is None or \
        gpt4ov2_ac is None or gpt4ov2_ve is None or gpt4ov2_fl is None or \
        gpt4ominiv2_ac is None or gpt4ominiv2_ve is None or gpt4ominiv2_fl is None:
        st.error("Informe todas as avaliações")
    else:
        st.session_state.num_processo.append(df["num_processo"][st.session_state.linha])
        st.session_state.gpt4ov1_a.append(gpt4ov1_ac)
        st.session_state.gpt4ov1_v.append(gpt4ov1_ve)
        st.session_state.gpt4ov1_f.append(gpt4ov1_fl)
        st.session_state.gpt4ominiv1_a.append(gpt4ominiv1_ac)
        st.session_state.gpt4ominiv1_v.append(gpt4ominiv1_ve)
        st.session_state.gpt4ominiv1_f.append(gpt4ominiv1_fl)
        # st.session_state.llamav1_a.append()
        # st.session_state.llamav1_v.append()
        # st.session_state.llamav1_f.append()
        st.session_state.gpt4ov2_a.append(gpt4ov2_ac)
        st.session_state.gpt4ov2_v.append(gpt4ov2_ve)
        st.session_state.gpt4ov2_f.append(gpt4ov2_fl)
        st.session_state.gpt4ominiv2_a.append(gpt4ominiv2_ac)
        st.session_state.gpt4ominiv2_v.append(gpt4ominiv2_ve)
        st.session_state.gpt4ominiv2_f.append(gpt4ominiv2_fl)
        # st.session_state.llamav2_a.append()
        # st.session_state.llamav2_v.append()
        # st.session_state.llamav2_f.append()

        st.session_state.linha += 1
        # st.write("linha = " + str(st.session_state.linha) + " " + str(datetime.now().strftime("%H:%M:%S:%f")))

        st.write("depois")
        st.write(st.session_state.gpt4ominiv1_a)

# Carregar o arquivo Excel
uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx"], on_change=inicializar_variaveis)

if uploaded_file is not None:
    st.write("linha = " + str(st.session_state.linha) + " " + str(datetime.now().strftime("%H:%M:%S:%f")))

    df = pd.read_excel(uploaded_file)

    if st.session_state.linha < len(df):
        # linha = st.session_state.linha
        # st.write("linha < len(df): linha = " + str(linha) + " " + str(datetime.now().strftime("%H:%M:%S:%f")))

        # st.header("Processo: " + df["num_processo"][st.session_state.linha])

        st.subheader("Relatório de sentença original")

        with st.container(height=300):
            st.markdown(df["reference"][st.session_state.linha])
            # st.markdown('<span style="font-size: 12px;">' + df["reference"][st.session_state.linha] + '</span>', unsafe_allow_html=True)

        st.subheader("Relatórios gerados por LLM")

        col1, col2 = st.columns([3, 1], vertical_alignment="center")
        # col1, col2 = st.columns([3, 1])

        with col1:
            with st.container(height=300):
                st.markdown(df["gpt-4o-v1"][st.session_state.linha])
                # st.markdown('<span style="font-size: 12px;">'+df["gpt-4o-v1"][st.session_state.linha]+'</span>', unsafe_allow_html=True)

        with col2:
            st.write("Acurácia")
            gpt4ov1_ac = st.feedback("faces", key="gpt4ov1_ac"+str(st.session_state.linha))
            st.write("Verdade")
            gpt4ov1_ve = st.feedback("faces", key="gpt4ov1_ve"+str(st.session_state.linha))
            st.write("Fluência")
            gpt4ov1_fl = st.feedback("faces", key="gpt4ov1_fl"+str(st.session_state.linha))

        st.divider()

        col1, col2 = st.columns([3, 1], vertical_alignment="center")

        with col1:
            with st.container(height=300):
                st.markdown(df["gpt-4o-mini-v1"][st.session_state.linha])
                # st.html('<span style="font-size: 12px;">'+df["gpt-4o-mini-v1"][st.session_state.linha]+'</span>')

        with col2:
            # gpt4ominiv1_ac = st.radio("Acurácia?", ("Sim", "Não"), key="gpt4ominiv1_ac")
            st.write("Acurácia")
            gpt4ominiv1_ac = st.feedback("stars", key="gpt4ominiv1_ac"+str(st.session_state.linha))
            st.write("Verdade")
            gpt4ominiv1_ve = st.feedback("stars", key="gpt4ominiv1_ve"+str(st.session_state.linha))
            st.write("Fluência")
            gpt4ominiv1_fl = st.feedback("stars", key="gpt4ominiv1_fl"+str(st.session_state.linha))

        st.divider()

        col1, col2 = st.columns([3, 1], vertical_alignment="center")

        with col1:
            with st.container(height=300):
                st.markdown(df["gpt-4o-v2"][st.session_state.linha])
                # st.html('<span style="font-size: 12px;">'+df["gpt-4o-v2"][st.session_state.linha]+'</span>')

        with col2:
            st.write("Acurácia")
            gpt4ov2_ac = st.feedback("stars", key="gpt4ov2_ac"+str(st.session_state.linha))
            st.write("Verdade")
            gpt4ov2_ve = st.feedback("stars", key="gpt4ov2_ve"+str(st.session_state.linha))
            st.write("Fluência")
            gpt4ov2_fl = st.feedback("stars", key="gpt4ov2_fl"+str(st.session_state.linha))

        st.divider()

        col1, col2 = st.columns([3, 1], vertical_alignment="center")

        with col1:
            with st.container(height=300):
                st.markdown(df["gpt-4o-mini-v2"][st.session_state.linha])
                # st.html('<span style="font-size: 12px;">'+df["gpt-4o-mini-v2"][st.session_state.linha]+'</span>')

        with col2:
            st.write("Acurácia")
            gpt4ominiv2_ac = st.feedback("stars", key="gpt4ominiv2_ac"+str(st.session_state.linha))
            st.write("Verdade")
            gpt4ominiv2_ve = st.feedback("stars", key="gpt4ominiv2_ve"+str(st.session_state.linha))
            st.write("Fluência")
            gpt4ominiv2_fl = st.feedback("stars", key="gpt4ominiv2_fl"+str(st.session_state.linha))

        st.button('Próximo processo', on_click=mostrar_proxima_linha, key='botao_mostrar_proxima_linha')

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

        df_respostas = pd.DataFrame(respostas)
        df_respostas.to_excel("Respostas.xlsx", index=False)

        # Ler o arquivo Excel gerado
        with open("Respostas.xlsx", "rb") as file:
            st.download_button(
                label="Salvar respostas",
                data=file,
                file_name=uploaded_file.name.split(".")[0]+"-respostas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

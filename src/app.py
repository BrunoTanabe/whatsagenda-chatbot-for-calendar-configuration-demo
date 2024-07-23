# app.py: Script para criar a interface do chatbot Aila

## IMPORTAÇÃO DOS PACOTES NECESSÁRIOS
### Pacotes do Python
import os
### Pacotes Locais
from functions import conversation_chain
from html_template import css, ai_template, human_template, hide_st_style
### Pacotes Streamlit
import streamlit as st
### Pacotes do LangChain
from langchain.schema import HumanMessage, AIMessage

## FUNÇÕES

### Função para gerar a página do chatbot
def generate_page():
    st.set_page_config(page_title="WhatsAgenda ChatBot",
        page_icon="./src/assets/favicon.ico", 
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.write(css, unsafe_allow_html=True)
    
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    with st.sidebar:
        st.image("./src/assets/vertical-logo.png", use_column_width=True)
        st.subheader("", divider="orange")
        st.subheader("")
        
        if os.path.exists("./data/vectorstore/"):
            st.success("A Aila está online e conectada com as informações do WhatsAgenda!")
        else:
            st.error(":warning: A Aila não conseguiu se conectar com as informações do WhatsAgenda!")
            
        if st.button("NOVA CONVERSA", use_container_width=True):
            del st.session_state["chat_history"]
            
    st.header(":speech_balloon: AILA ChatBot", anchor="chat", divider="orange")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
        welcome_message = "Olá! Sou a **Aila**, sua assistente amigável e experiente do **WhatsAgenda**! :smile:\n\nEstou aqui para te ajudar a usar a nossa plataforma e configurar suas agendas. Vamos transformar sua organização diária em uma experiência simples e produtiva! :rocket: \n\n**Como posso te ajudar hoje?**"
        st.session_state["chat_history"].extend(
            [
                AIMessage(content=welcome_message),
            ]
        )
        # st.write(ai_template.replace("{{MSG}}", "\n\n" + welcome_message), unsafe_allow_html=True)
    
    if user_message := st.chat_input(placeholder="Como a Aila pode te ajudar hoje?"):
        st.session_state["chat_history"].extend(
            [
                HumanMessage(content=user_message),
            ]
        )
        # st.write(human_template.replace("{{MSG}}", "\n\n" + user_message), unsafe_allow_html=True)
        
        llm_response = ""
        for chunk in conversation_chain(user_message, st.session_state["chat_history"]):
            llm_response += chunk
            # st.write_stream(conversation_chain(user_message, st.session_state["chat_history"]))
            # print(chunk, end="", flush=True)
        # print(llm_response)
        st.session_state["chat_history"].extend(
            [
                AIMessage(content=llm_response),
            ]
        )
        # st.write(ai_template.replace("{{MSG}}", "\n\n" + message.content), unsafe_allow_html=True)
    
    for message in st.session_state["chat_history"]:
        if isinstance(message, HumanMessage):
            st.write(human_template.replace("{{MSG}}", "\n\n" + message.content), unsafe_allow_html=True)
        elif isinstance(message, AIMessage):
            st.write(ai_template.replace("{{MSG}}", "\n\n" + message.content), unsafe_allow_html=True)

## EXECUÇÃO DO SCRIPT             
if __name__ == "__main__":
    generate_page()
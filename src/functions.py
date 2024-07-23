# functions.py: Script para criar a função de conversação do chatbot Aila

## IMPORTAÇÃO DOS PACOTES NECESSÁRIOS

### Pacotes Locais
from models import llama3_model
### Pacotes do LangChain
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever

## FUNÇÕES

### Função para criar a cadeia de conversação do chatbot
def conversation_chain(user_message, chat_history):
    
    chat_llm = llama3_model
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.load_local("./data/vectorstore", embeddings, allow_dangerous_deserialization=True)
    retriever=vectorstore.as_retriever()
    
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    history_aware_retriever = create_history_aware_retriever(
        chat_llm, retriever, contextualize_q_prompt
    )
    
    system_prompt = (
        "You are Aila, the friendly and knowledgeable assistant for WhatsAgenda. "
        "Your task is to help WhatsAgenda customers use the platform effectively "
        "and set up their schedules efficiently. Use the following pieces of retrieved "
        "context to answer their questions accurately and clearly. Always provide "
        "step-by-step guidance when necessary and offer additional tips to enhance "
        "their experience. Always respond in Brazilian Portuguese and using best "
        "markdown (.md) formatting practices and emojis."
        "\n\n"
        "{context}"
    )
    
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    question_answer_chain = create_stuff_documents_chain(chat_llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    # response = rag_chain.invoke({"input": user_message, "chat_history": chat_history})
    # return response["answer"]
    
    for chunk in rag_chain.stream({"input": user_message, "chat_history": chat_history}):   
        if answer_chunk := chunk.get("answer"):
            yield answer_chunk
            
    return
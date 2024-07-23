# vectorstore-create.py: Script para criar um vetor de embeddings de um documento PDF

## IMPORTAÇÃO DOS PACOTES NECESSÁRIOS
### Pacotes do Python
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
### Pacotes do LangChain
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

## CARREGAMENTO DAS VARIÁVEIS DE AMBIENTE
### Ajuste do caminho para o arquivo .env e importação das variáveis de ambiente
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(dotenv_path)

## FUNÇÕES

### Função para extrair o conteúdo de um documento PDF
def get_pdf_content(documents):
    raw_text = ""

    for document in documents:
        pdf_reader = PdfReader(document)
        for page in pdf_reader.pages:
            raw_text += page.extract_text()

    return raw_text

### Função para dividir o texto em pedaços menores
def get_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    text_chunks = text_splitter.split_text(text)
    
    return text_chunks

### Função para criar um vetor de embeddings a partir dos pedaços de texto
def get_embeddings(chunks):
    embeddings = HuggingFaceEmbeddings()
    vector_storage = FAISS.from_texts(texts=chunks, embedding=embeddings)

    return vector_storage

### Função principal
def main(documents):
    raw_text = get_pdf_content(documents)
    chunks = get_chunks(raw_text)
    vector_storage = get_embeddings(chunks)
    vector_storage.save_local("./data/vectorstore")
    
    return

## EXECUÇÃO DO SCRIPT
if __name__ == "__main__":
    document_path = ["./data/whatsagenda-data.pdf"]
    main(document_path)
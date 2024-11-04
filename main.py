import os
from dotenv import load_dotenv 
load_dotenv() 
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

FILE_PATH = ("dataset/BOOKS/CM_ALE_aooo_004_OCR.pdf")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TXT_FILE = 'dataset/output/CM_ALE_aooo_004_OCR.txt'

def len_func(text):
    return len(text)

def main():               
    loader = PyPDFLoader(FILE_PATH)
    pages = []
    for page in loader.lazy_load():
        pages.append(page)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002",
    )

    with open(TXT_FILE,'r') as f:
        hp_book = f.read()

    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size = 1200,
        chunk_overlap = 100,
        length_function = len_func,
        is_separator_regex= False)

    para_list = text_splitter.create_documents(texts = [hp_book])
    docs = text_splitter.split_documents(para_list)

    # Embeddings
    single_vector = embeddings.embed_query(docs[1])
    print(str(single_vector)[:100])

if __name__ == "__main__":
    main()
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from tqdm import tqdm
import json
import os
import re

load_dotenv(".env")

BOOKS_FOLDER = "dataset/BOOKS/"
JSON_FOLDER = "dataset/JSON_FILES/"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELASTIC_POST_HOST = os.getenv("ELASTIC_HOST")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
ELASTIC_PWD = os.getenv("ELASTIC_PWD")
CA_CERTS = os.getenv("CA_CERTS_PATH")

CLIENT = Elasticsearch(
  ELASTIC_POST_HOST,
  basic_auth=(ELASTIC_USERNAME, ELASTIC_PWD),
  ca_certs=CA_CERTS
)

EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

# Remove unwanted special characters (such as strange symbols) but keep punctuation (.,;:) and the apostrophe
def clean_text(text):
    text = re.sub(r"[^\w\s.,;:'']", '', text)  
    text = re.sub(r'[•~^$%\*&@!\\/\t]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    text = re.sub(r'(?<=\n)\n', '', text)
    text = re.sub(r'\n+', '\n', text)
    return text

def len_func(text):
    return len(text)

text_splitter = CharacterTextSplitter(
    separator= ".",
    chunk_size=1200,
    chunk_overlap=100,
    length_function=len_func,
    is_separator_regex=False
)

def main() -> object:
    for book_name in os.listdir(BOOKS_FOLDER):
        book_json_folder = os.path.join(JSON_FOLDER, book_name.replace(".pdf", ""))
        if not os.path.exists(book_json_folder):
            os.mkdir(book_json_folder)
            print(f" > Creating {book_json_folder} folder")
            print(f" > Reading book: {book_name}")
            loader = PyPDFLoader(os.path.join(BOOKS_FOLDER, book_name))
            pages = []
            metadata_l = []
            for single_page in loader.lazy_load():
                page = json.loads(single_page.model_dump_json())
                pages.append(clean_text(page["page_content"]))
                metadata_l.append({
                    "source_file": page["metadata"]["source"].split("/")[-1],
                    "page_number": page["metadata"]["page"]
                })

            para_list = text_splitter.create_documents(texts=pages,
                                                       metadatas=metadata_l)

            for i, document in tqdm(enumerate(para_list), total=len(para_list), desc=" > Generating embeddings"):
                doc = json.loads(document.model_dump_json())
                elastic_document = {
                    "id": doc["metadata"]["source_file"] + "_" + str(doc["metadata"]["page_number"]) + "_" + str(i),
                    "source_file": doc["metadata"]["source_file"],
                    "page_number": doc["metadata"]["page_number"],
                    "plain_text": doc["page_content"],
                    "embeddings": EMBEDDINGS.embed_query(doc["page_content"])
                }

                resp = CLIENT.index(index="llm-index", id=elastic_document["id"],
                                    document=elastic_document)
                with open(os.path.join(book_json_folder,
                                       f"""page_{elastic_document['id']}_{resp["result"]}"""), 'w') as fp:
                    json.dump(elastic_document, fp)
        else:
            print(f" > Book {book_name} already indexed")

if __name__ == "__main__":
    main()
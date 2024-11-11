from langchain_openai import OpenAI, OpenAIEmbeddings
from elasticsearch import Elasticsearch
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(".env")

elastic_port_path = os.getenv("ELASTIC_HOST")
elastic_username = os.getenv("ELASTIC_USERNAME")
elastic_pwd = os.getenv("ELASTIC_PWD")
ca_certs = os.getenv("CA_CERTS_PATH")

CLIENT = Elasticsearch(
  elastic_port_path,
  basic_auth=(elastic_username, elastic_pwd),
  ca_certs=ca_certs
)

EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

# Get user prompt to feed into the LLM.
# user_prompt = input(" > Ask me anything about design.\n")

# Create embedding for the user prompt
def relevant_documents(user_prompt):
    user_prompt_embeddings = EMBEDDINGS.embed_query(user_prompt)

    resp = CLIENT.knn_search(
        index="llm-index",
        knn={
            "field": "embeddings",
            "query_vector": user_prompt_embeddings,
            "k": 10,
            "num_candidates": 100
        },
        source=[
            "plain_text",
            "id"
        ],
    )

    template = f"""
    These Human will ask you a questions about design. 
    Use following piece of context to answer the question. 
    If you don't know the answer, just say you don't know. 
    Keep the answer within 2 sentences and concise, according to the question language.

    Context: {resp['hits']['hits'][0:3]}
    Question: {user_prompt}
    Answer: 
    """

    print(resp['hits']['hits'])
    return template
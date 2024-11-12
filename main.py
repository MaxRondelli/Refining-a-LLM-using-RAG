from langchain_openai import OpenAIEmbeddings
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
load_dotenv(".env")

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

    # The interval [0:3] means we're going to take only three documents around the user_prompt embedding.
    context = resp['hits']['hits'][0:3]

    template = f"""
    These Human will ask you a questions about design. 
    Use following piece of context to answer the question. 
    If you don't know the answer, just say you don't know. 
    Keep the answer within 2 sentences and concise, according to the question language.

    Context: {context}
    Question: {user_prompt}
    Answer: 
    """

    print(resp['hits']['hits'])
    return template
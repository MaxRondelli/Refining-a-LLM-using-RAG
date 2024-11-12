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

# Set up the configuration for the elastic index database
index_name = "llm-index"
index_settings = {
    "number_of_shards": 1
  }
index_mapping = {
  "properties": {
    "source_file": {"type": "keyword"},
    "page_number": {"type": "long"},
    "plain_text": {"type": "text"},
    "embeddings": {
      "type": "dense_vector",
      "dims": 3072
    }
  }
}

res = CLIENT.indices.create(index=index_name, mappings=index_mapping, settings=index_settings)

print(res)
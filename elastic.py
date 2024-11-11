from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
load_dotenv(".env")

elastic_port_path = os.getenv("ELASTIC_HOST")
elastic_username = os.getenv("ELASTIC_USERNAME")
elastic_pwd = os.getenv("ELASTIC_PWD")
ca_certs = os.getenv("CA_CERTS_PATH")

client = Elasticsearch(
  elastic_port_path,
  basic_auth=(elastic_username, elastic_pwd),
  ca_certs=ca_certs
)

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


res = client.indices.create(index=index_name, mappings=index_mapping, settings=index_settings)

print(res)
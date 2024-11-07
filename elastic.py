from elasticsearch import Elasticsearch 
import os 
from dotenv import load_dotenv 
load_dotenv() 

elastic_port_path = os.getenv("ELASTIC_HOST")
elastic_username = os.getenv("ELASTIC_USERNAME")
elastic_pwd = os.getenv("ELASTIC_PWD")
ca_certs = os.getenv("CA_CERTS_PATH")

client = Elasticsearch(
  elastic_port_path,
  basic_auth=(elastic_username, elastic_pwd),
  ca_certs=ca_certs
)

client.info()

documents = [
  { "index": { "_index": "index_name", "_id": "9780553351927"}},
  {"name": "Snow Crash", "author": "Neal Stephenson", "release_date": "1992-06-01", "page_count": 470},
  { "index": { "_index": "index_name", "_id": "9780441017225"}},
  {"name": "Revelation Space", "author": "Alastair Reynolds", "release_date": "2000-03-15", "page_count": 585},
  { "index": { "_index": "index_name", "_id": "9780451524935"}},
  {"name": "1984", "author": "George Orwell", "release_date": "1985-06-01", "page_count": 328},
  { "index": { "_index": "index_name", "_id": "9781451673319"}},
  {"name": "Fahrenheit 451", "author": "Ray Bradbury", "release_date": "1953-10-15", "page_count": 227},
  { "index": { "_index": "index_name", "_id": "9780060850524"}},
  {"name": "Brave New World", "author": "Aldous Huxley", "release_date": "1932-06-01", "page_count": 268},
  { "index": { "_index": "index_name", "_id": "9780385490818"}},
  {"name": "The Handmaid's Tale", "author": "Margaret Atwood", "release_date": "1985-06-01", "page_count": 311},
]

client.bulk(operations=documents)
client.search(index="index_name", q="snow")
# Refining-a-LLM-using-RAG
The goal of this project is to create a system for refining Large Language Models (LLMs) using Retrieval-Augmented Generation (RAG). It implements a design assistant that leverages GPT-4 and ElasticSearch to provide contextually relevant design advice. 

<div align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1400/1*bo0JwTdru5quxDiPFa1TvA.png" alt="Alt Text" width="640" height="480">
</div>

## Prerequisites

- OpenAI API key
- ElasticSearch instance
- Kibana
- Python 3.8+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MaxRondelli/Refining-a-LLM-using-RAG.git
cd Refining-a-LLM-using-RAG
```
2. Install required dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file in the root directory with your credentials:
```env
OPENAI_API_KEY=your_openai_api_key
ELASTIC_HOST=your_elasticsearch_host
CA_CERTS_PATH=ca_certs_path
ELASTIC_USERNAME=your_username
ELASTIC_PWD=your_password
```

## Project's Structure
- `webapp.py`: Streamlit-based user interface and chat logic
- `main.py`: Core functionality for document retrieval and prompt generation
- `indexer.py`: Document processing and embedding generation
- `elastic.py`: ElasticSearch database configuration and operations

## Project's Pipeline
### Document Indexing
The system processes PDF documents through the following steps:
- Splits documents into manageable chunks.
- Generates embeddings for each chunk using OpenAI's embedding model.
- Stores the embeddings and text in ElasticSearch.
### Query Processing
When a user submits a query:
- The system generates an embedding for the query.
- Searches for the 3 most relevant document chunks using k-NN search.
- Creates a prompt template combining the query and relevant context.
### Response Generation
The system:
- Maintains conversation history for context.
- Uses GPT-4 to generate responses based on retrieved documents.
- Presents responses through a user-friendly interface.

## Usage
1. Create the vector database running the
```bash
python3 elastic.py
```
Be sure the docker with elastic and kibare are on.  

2. Index the new documents with
```bash
python3 indexer.py
```
3. Start the web application with
```bash
streamlit run webapp.py
```

## Contributing
The project has been developed between me and [Alessandro Borrelli](https://github.com/aleborrelli).

Contributions are welcome! Feel free to submit PRs.

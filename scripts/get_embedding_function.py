from langchain_community.embeddings.ollama import OllamaEmbeddings

def get_embedding_function():
    embeddings = OllamaEmbeddings(base_url='http://ollama:11434', 
                                  model="nomic-embed-text")
    return embeddings

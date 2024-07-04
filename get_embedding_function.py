from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_community.embeddings.huggingface import HuggingFaceInstructEmbeddings
from langchain_community.embeddings import OllamaEmbeddings


def get_embedding_function():
    # embeddings = BedrockEmbeddings(
    #     credentials_profile_name="default", region_name="us-east-1"
    # )
    embeddings = OllamaEmbeddings(base_url='http://127.0.0.1:11434', 
                                  model="nomic-embed-text")
    # embeddings = HuggingFaceInstructEmbeddings(model="hkunlp/instructor-large")
    return embeddings

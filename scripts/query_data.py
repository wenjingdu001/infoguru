from langchain_community.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from scripts.get_embedding_function import get_embedding_function


def query_rag(query_text: str):
    CHROMA_PATH = "data/chroma"

    PROMPT_TEMPLATE = """
    Answer the question based on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}.
    If the above context cannot answer the question, clearly state that and come up with a answer based on your knowledge.
    """
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = Ollama(model="llama3.1:8b", base_url="http://ollama:11434")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\n\nSources: {sources}"
    # print(formatted_response)

    response_dict = dict()
    response_dict["response"] = response_text
    response_dict["source"] = "\n\n---\n\n".join([s for s in sources])
    return response_dict

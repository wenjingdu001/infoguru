import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters.markdown import MarkdownHeaderTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata

from pathlib import Path


CHROMA_PATH = "data/chroma"
DATA_PATH = "data/source_doc"

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    # documents = load_documents()
    chunks = directory_loader(DATA_PATH)
    add_to_chroma(chunks)

def pdf_loader(file):
    try:
        loader = PyPDFLoader(str(file))
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = str(file)
    except Exception as e:
        raise e
    return docs

def txt_loader(file):
    try:
        loader = TextLoader(str(file), encoding='utf-8')
        doc = loader.load()
        doc = doc[0]
        doc.metadata["source"] = str(file)
    except Exception as e:
        raise e
    return doc

def directory_loader(path):
    p = Path(path)
    chunks = []
    
    text_items = p.rglob("**/[!.]*.txt") 
    for i in text_items:
        print(i)
        doc = txt_loader(i)
        sub_chunks = split_documents(doc, 'txt')
        chunks.extend(sub_chunks)    
    
    pdf_items = p.rglob("**/[!.]*.pdf")
    for i in pdf_items:
        print(i)
        doc = pdf_loader(i)
        sub_chunks = split_documents(doc, 'pdf')
        chunks.extend(sub_chunks)

    md_items = p.rglob("**/[!.]*.md")
    for i in md_items:
        doc = txt_loader(i)
        sub_chunks = split_documents(doc, 'md')
        chunks.extend(sub_chunks) 
    
    return chunks

def split_documents(documents: Document, file_type):
    if file_type=='md':
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
        ]
        text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers = False)
        return text_splitter.split_text(documents.page_content)
    else:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        return text_splitter.split_documents([documents])


def add_to_chroma(chunks: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()
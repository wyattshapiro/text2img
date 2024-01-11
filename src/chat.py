import os
import json
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')


def construct_index(directory_data, directory_index, force_reload=False):
    # check if storage already exists
    if not os.path.exists(directory_index) or force_reload:
        print(f'Creating new index using {directory_data}')
        # load the documents and create the index
        documents = SimpleDirectoryReader(directory_data).load_data()
        index = VectorStoreIndex.from_documents(documents)
        # store it for later
        index.storage_context.persist(persist_dir=directory_index)
        print(f'Storing new index to {directory_index}')
    else:
        # load the existing index
        print(f'Loading existing index from {directory_index}')
        storage_context = StorageContext.from_defaults(persist_dir=directory_index)
        index = load_index_from_storage(storage_context)
    
    return index

def query(question, index):
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return response

def get_quote_from_category(category):
    index = construct_index(directory_data=f'data/quotes', directory_index=f'storage/quotes')
    query_engine = index.as_query_engine()
    request = f"Return a single quote in json format that is in the {category} category. If category is not found, then look up a new quote and return in json format."
    print("requesting quote")
    response = query_engine.query(request)
    response_json = json.loads(str(response))
    return response_json

def get_category_from_text(text):
    CATEGORIES = ["Actionable", "Analytical", "Contrarian", "Motivational", "Observational", "Future", "Other"]
    index = construct_index(directory_data=f'data/quotes', directory_index=f'storage/quotes')
    query_engine = index.as_query_engine()
    request = f"Which category out of {CATEGORIES} is the most relevant to the following text. If Other please specify a one word category that summarizes the text. {text}"
    print("requesting category from text")
    response = query_engine.query(request)
    # response_json = json.loads(str(response))
    # print(response_json)
    return response

def test_ask():
    index = construct_index(directory_data=f'data/quotes', directory_index=f'storage/quotes', force_reload=True)
    while True:
        question = input("Get category from text")
        if question == 'quit':
            break
        # response = query(question=question, index=index)
        category = get_category_from_text(question)
        print(f"chosen category: {category}")
        quote = get_quote_from_category(question)
        print(f"chosen quote: {quote}")

if __name__ == '__main__':
    test_ask()
    
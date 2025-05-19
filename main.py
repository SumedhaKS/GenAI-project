from wikipedia_info import get_institution_info
from document_chat import run_document_chat
from cohere_chain import ask_with_prompt
import os

def run_app():
    print("Welcome to GenAI Institution Assistant!")
    query = input("Enter an institution name OR path to a document (.txt/.pdf): ")
    print(query , "\n")
    if query.endswith(".pdf") or query.endswith(".txt"):
        run_document_chat(query)
    else:
        info = get_institution_info(query)
        response = ask_with_prompt(info)
        print("\nStructured Institution Info:\n")
        print(response)

if __name__ == "__main__":
    run_app()

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import CohereEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatCohere
from langchain_community.document_loaders import TextLoader
import os
import PyPDF2

def load_document(path):
    if path.endswith(".pdf"):
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    else:
        loader = TextLoader(path)
        text = loader.load()[0].page_content
    return text

def run_document_chat(path):
    text = load_document(path)

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.create_documents([text])

    embeddings = CohereEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    retriever = db.as_retriever()

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = ChatCohere()

    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

    print("\nYou can now chat with your document! Type 'exit' to quit.\n")
    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            break
        result = qa_chain.run(question)
        print(f"Bot: {result}\n")

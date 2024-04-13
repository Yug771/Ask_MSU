from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore
import os
import time
from dotenv import load_dotenv
load_dotenv()

from pinecone import Pinecone, ServerlessSpec
pinecone_api_key = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=pinecone_api_key)
# print(pc.describe_index("msu-data"))
index = pc.Index("msu-data")

embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
text_field = "text"
vectorstore = PineconeVectorStore(
    index, embeddings, text_field
)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

def get_conversational_chain():

    prompt_template = """
    You are an Artificial Intelligence powered chatbot, you are here to answer questions about Maharaja sayajirao University.
    Answer the question as detailed as possible from the provided context, make sure to provide the very detailed, accurate and to the point answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def answer_question(question_text):

    docs = vectorstore.similarity_search(
    query = question_text,  # our search query
    k=10
    )
    print(f"\n\nRetrived context: {docs}\n\n\n")
    chain = get_conversational_chain()
    response = chain(
        {"input_documents":docs, "question": question_text}
        , return_only_outputs=True)
    print(f"Answer: {response['output_text']}\n\n")
    return response['output_text']
    # time.sleep(5)
    # return "This is a test answer"
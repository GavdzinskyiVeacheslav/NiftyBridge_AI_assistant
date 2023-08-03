import math
import os
from dotenv import load_dotenv
import tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain

# Additional constants
ENCODING = tiktoken.get_encoding("cl100k_base")
MAX_TOKENS_SUMMARY = 4096

# ENV
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# OpenAI model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
embeddings = OpenAIEmbeddings()

# PDF
loader = PyPDFLoader("service_terms.pdf")
pages = loader.load_and_split()

# Bot settings
SUMMARY_SYS_MSG = """You are Nifty Bridge AI assistant. You have to introduce yourself as Nifty Bridge AI assistant. 
Use the following pieces of context to answer the users question. 
If you cannot answer, just say ""I don't know please contact with support 
by email support@nifty-bridge.com", don't try to make up an answer."""

# Splitter
text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
      )

# Chunks
text_chunks = text_splitter.split_text(SUMMARY_SYS_MSG)

# Vectorstore
knowledge_base = FAISS.from_texts(text_chunks, embeddings)


# Auxiliary functions for processing max_tokens
def token_len(user_input: str) -> int:
    """Get token length for openai"""
    return len(ENCODING.encode(user_input))


def chunk(user_input: str) -> list:
    input_tokens = token_len(user_input)
    count = math.ceil(input_tokens / MAX_TOKENS_SUMMARY)
    k, m = divmod(len(user_input), count)
    chunks = [
        user_input[i * k + min(i, m): (i + 1) * k + min(i + 1, m)] for i in range(count)
    ]
    return chunks


def summarize(user_input: str) -> str:
    system_message = SystemMessagePromptTemplate.from_template(
        template=SUMMARY_SYS_MSG
    )
    human_message = HumanMessagePromptTemplate.from_template(
        template="Input: {input}"
    )

    chunks = chunk(user_input=user_input)

    summary = ""

    for i in chunks:
        prompt = ChatPromptTemplate(
            input_variables=["input"],
            messages=[system_message, human_message],
        )

        _input = prompt.format_prompt(input=i)
        output = llm(_input.to_messages())
        summary += f"\n{output.content}"

    sum_tokens = token_len(user_input=summary)

    if sum_tokens > MAX_TOKENS_SUMMARY:
        return summarize(user_input=summary)

    return summary


def openai_answers(message):
    """Main answer function that get user message.
    Perform similarity search in the vectorstore and generate the answer."""

    user_question = summarize(message)
    docs = knowledge_base.similarity_search(user_question)
    chain = load_qa_chain(llm)
    response = chain.run(input_documents=docs, question=user_question)

    return response

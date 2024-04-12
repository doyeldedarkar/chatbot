import textract
from transformers import GPT2TokenizerFast
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os

import textract
doc = textract.process("./input.json")

#Step 2: Save to .txt and reopen (helps prevent issues)
with open('input.txt', 'w', encoding='utf-8') as f:
    f.write(doc.decode('utf-8'))


with open('input.txt', 'r', encoding='utf-8') as f:
    pages = f.read()


with open('merged_db.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Step 3: Create function to count tokens
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

# Step 4: Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 512,
    chunk_overlap  = 24,
    length_function = count_tokens,
)

chunks = text_splitter.create_documents([text])

def test_embed():
    embeddings = OpenAIEmbeddings(openai_api_key=api)
    # Indexing
    # Save in a Vector DB
    index = FAISS.from_documents(chunks, embeddings)
    return index


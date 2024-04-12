# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 11:48:43 2023

@author: doyel
"""

import os
import textract
from transformers import GPT2TokenizerFast
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
from CTGChatbot.API import API_data


def updated_db():# Step 1: Convert PDF to text
    load_dotenv()
        
    try:
        doc = textract.process("./new_input.json")
        print("Succesfully processed")
    except:
        print("Error in processing")
        
    # Step 2: Save to .txt and reopen (helps prevent issues)
    with open('input.txt', 'w', encoding='utf-8') as f:
        f.write(doc.decode('utf-8'))
            
    with open('input.txt', 'r', encoding='utf-8') as f:
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
            
    # Get embedding model
    embeddings = OpenAIEmbeddings(chunk_size = 1)
    # Create vector database
    db = FAISS.from_documents(chunks, embeddings)
    #Load local vector store
    new_db = FAISS.load_local("../faiss_index", embeddings)
    #merge vectorstore
    new_db.merge_from(db)
    #save the updated vectorstore locally
    new_db.save_local("../faiss_index")
    print('Database is updated')
    os.remove("./new_data.json")
    os.remove("./merged_db.txt")

updated_db()

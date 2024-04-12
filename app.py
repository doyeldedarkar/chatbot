# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 10:48:32 2023

@author: DED5BUE
"""

import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import  ConversationalRetrievalChain
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
import streamlit as st
from PIL import Image
from dotenv import load_dotenv

def load_db():
    embeddings = OpenAIEmbeddings(chunk_size = 1)
    db = FAISS.load_local("faiss_index", embeddings)
    return db

    
def get_text():
    """
    Get the user input text.
    Returns:
        (str): The text entered by the user
    """

    input_text = st.text_input("What's on your mind ", st.session_state["input"], 
                               key="input",
                               placeholder="Ask me anything...",
                               label_visibility='hidden')
    return input_text

    
def clear_conv():
    """
    Clears the stored converstaions.
    """
    del st.session_state.stored_session

def new_chat():
    """
    Clears session state and starts a new chat.
    """
    save = []
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state.entity_memory.buffer.clear()

    
def main():
    
    load_dotenv()
    db = load_db()

    My_ICON = Image.open('My_logo.jpg')
    st.set_page_config(
        page_title="Tailored chatbot",
        page_icon=My_ICON,
        layout="wide")
    
    st.sidebar.title("Welcome to my customed made chatbot :blue_heart: ")

    
    st.sidebar.button("New Chat", on_click = new_chat, type='primary')
    
    #docs = db.similarity_search(query)
    
    
    llm = AzureChatOpenAI(
    deployment_name="gpt-35-turbo",
    model_name="gpt-4",
    temperature=0.7,
    openai_api_base=os.environ["OPENAI_API_BASE"],
    openai_api_type=os.environ["OPENAI_API_TYPE"],
    openai_api_key= os.environ["OPENAI_API_KEY"],
    )
    
    retriever = db.as_retriever(search_type = "similarity", search_kwargs = {"K":10})
    chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)
    
    
    
    if 'something' not in st.session_state:
        st.session_state.something = ''
    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []
    if "input" not in st.session_state:
        st.session_state["input"] = ""
    if "stored_session" not in st.session_state:
        st.session_state["stored_session"] = []
    if 'entity_memory' not in st.session_state:
        st.session_state.entity_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
           

    chat_history = []

    query = get_text() 
    if query:
        with st.spinner("Generating Answer to your Query : `{}` ".format(query)):
            st.session_state.past.append(query)
            response = chain({"question": query, "chat_history": chat_history})
            chat_history.append((query, response['answer']))
            st.session_state.generated.append(response['answer'])
        
        download_chat = []
        with st.expander("Conversation", expanded=True):
            for i in range(len(st.session_state['generated'])-1, -1, -1):
                st.info(st.session_state["past"][i],icon="🧐")
                st.success(st.session_state["generated"][i], icon="💻")
                download_chat.append(st.session_state["past"][i])
                download_chat.append(st.session_state["generated"][i])
            CHAT = '\n'.join(x for x in download_chat)
            st.download_button('Download',CHAT)

    for i, sublist in enumerate(st.session_state.stored_session):
        with st.sidebar.expander(label= f"Conversation-Session:{i}"):
            st.write(sublist)
    
    # Allow the user to clear all stored conversation sessions
    if st.session_state.stored_session:
        st.sidebar.button("Clear-all",on_click=clear_conv,type='primary')

main()

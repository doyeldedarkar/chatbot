"""  Main module for chatbot  """

#pylint: disable=redefined-outer-name
import os
import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import AzureChatOpenAI
from dotenv import load_dotenv

from config.prompts import (
    MENU_ITEMS,
    PAGE_ICON,
    TITLE,
    DATA_PROTECTION_MESSAGE,
    My_IMAGE
)

def get_text():
    """
    Get the user input text.
    Returns:
        (str): The text entered by the user
    """
    input_text = st.text_input("You: ", st.session_state["input"], key="input",
                            placeholder="Your AI assistant here! Ask me anything ...",
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
    #st.session_state.entity_memory.store = {}
    st.session_state.entity_memory.buffer.clear()

def main():
    load_dotenv()
    st.set_page_config(
        page_title=TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
        menu_items=MENU_ITEMS,  # type: ignore
    )
    
    st.title("ED's ChatBot")
    st.sidebar.image(ED_IMAGE)
    st.sidebar.button("New Chat", on_click = new_chat, type='primary')
    
    expand = st.sidebar.expander(" 🛠️ Settings ", expanded=False)
    with expand:
        st.write(DATA_PROTECTION_MESSAGE)
        MODEL = st.selectbox(label='Available Models', 
                             options=['gpt-4', 
                                      'gpt-3.5-turbo', 
                                      'Writer/InstructPalmyra-20b',
                                      'HuggingFaceH4/starchat-beta', 
                                      'databricks-dolly-v2-12b-4',
                                      'meta-llama/Llama-2-13b-chat-hf', 
                                      'tiiuae/falcon-7b-instruct', 
                                      'mosaicml/mpt-30b-instruct'])
#        K = st.slider('Summary of prompts to consider',min_value=1, value=5, max_value=20)
        temp = st.slider('Temperature(randomness of answer): ', min_value=0.0, value=0.7,
                               step=.1, max_value=1.0)
        max_tokens = st.slider('Max. Tokens: ',min_value=10, step=10, value=500,
                                     max_value=1000)
    
    
    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []
    if "input" not in st.session_state:
        st.session_state["input"] = ""
    if "stored_session" not in st.session_state:
        st.session_state["stored_session"] = []
    
    llm = AzureChatOpenAI(deployment_name="gpt-35-turbo",
                          temperature=temp,
                          openai_api_key=os.environ["OPENAI_API_KEY"],
                          openai_api_type=os.environ["OPENAI_API_TYPE"],
                          openai_api_base =os.environ["OPENAI_API_BASE"],
                          openai_api_version = os.environ["OPENAI_API_VERSION"],
                          model_name=MODEL,
                          max_tokens=max_tokens,
                          verbose=False)
    
    
        # Create a ConversationEntityMemory object if not already created
    if 'entity_memory' not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=10 )
    
            # Create the ConversationChain object with the specified configuration
    Conversation = ConversationChain(
        llm=llm,
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=st.session_state.entity_memory
        )
    
    
    user_input = get_text()
    
    if user_input:
        output = Conversation.run(input=user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)
    
    download_chat = []
    with st.expander("Conversation", expanded=True):
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            st.info(st.session_state["past"][i],icon="🧐")
            st.success(st.session_state["generated"][i], icon="🤖")
            download_chat.append(st.session_state["past"][i])
            download_chat.append(st.session_state["generated"][i])
        CHAT = '\n'.join(x for x in download_chat)
        st.download_button('Download',CHAT)
    
    #Display stored conversation sessions in the sidebar
    for i, sublist in enumerate(st.session_state.stored_session):
        with st.sidebar.expander(label= f"Conversation-Session:{i}"):
            st.write(sublist)
    
    # Allow the user to clear all stored conversation sessions
    if st.session_state.stored_session:
        st.sidebar.button("Clear-all",on_click=clear_conv,type='primary')
 
main()

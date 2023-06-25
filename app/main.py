"""Python file to serve as the frontend"""
import os
import streamlit as st
from PIL import Image
import base64
from langchain.memory import ConversationBufferWindowMemory
from dataclasses import dataclass
from typing import Literal
import llm
import sidebar as sb

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

###################### FUNCTION DEFINITIONS ##############################

@dataclass
class Message:
    """Class for keeping track of a chat message."""
    origin: Literal["human", "ai"]
    message: str

@st.cache_data(show_spinner=False)
def get_local_img(file_path: str) -> str:
    # Load a byte image and return its base64 encoded string
    return base64.b64encode(open(file_path, "rb").read()).decode("utf-8")

@st.cache_data(show_spinner=False)
def get_favicon(file_path: str):
    # Load a byte image and return its favicon
    return Image.open(file_path)
    
favicon = get_favicon(os.path.join(ROOT_DIR, "app", "static", "ai_icon.png"))
st.set_page_config(page_title="ChatGPT Assistant", page_icon=favicon)


def load_css():
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

load_css()


############################### Main body #################################
st.title("ChatGPT Assistant")

sb.sidebar_setup()

if "history" not in st.session_state:
    st.session_state.history = []

if "model" not in st.session_state:
    st.session_state.model = "chat-bison"
    # Create a memory object if not already created
    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationBufferWindowMemory(k=3,return_messages=True)
    st.session_state.conversation = llm.load_chat(st.session_state.model,0.2,1024,0.8,40,st.session_state.memory)


chat_placeholder = st.container()

#Define how each user and AI bubble will look like in the chat
with chat_placeholder:
    for chat in st.session_state.history:
        if chat.origin == 'ai':
            file_path = os.path.join(ROOT_DIR, "app", "static", "ai_icon.png")
            div = f"""
                    <div class="chat-row">
                        <img class="chat-icon" src="{f"data:image/gif;base64,{get_local_img(file_path)}"}"
                            width=32 height=32>
                        <div class="chat-bubble ai-bubble">
                            &#8203;{chat.message}
                        </div>
                    </div>
                    """
        else:
            file_path = os.path.join(ROOT_DIR, "app", "static", "user_icon.png")
            div = f"""
                    <div class="chat-row row-reverse">
                        <img class="chat-icon" src="{f"data:image/gif;base64,{get_local_img(file_path)}"}"
                            width=32 height=32>
                        <div class="chat-bubble human-bubble">
                            &#8203;{chat.message}
                        </div>
                    </div>
                    """
        st.markdown(div, unsafe_allow_html=True)

    for _ in range(3):
        st.markdown("")

#Function to call the LLM when the button is clicked then adding the request/response to the session history
def on_click_callback():
    with chat_placeholder:
        writing_animation = st.empty()
        file_path = os.path.join(ROOT_DIR, "app", "static", "loading.gif")
        writing_animation.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;<img src='data:image/gif;base64,{get_local_img(file_path)}' width=30 height=10>", unsafe_allow_html=True)
    human_prompt = st.session_state.human_prompt
    llm_response = st.session_state.conversation.run(
        human_prompt
    )
    st.session_state.history.append(
        Message("human", human_prompt)
    )
    with chat_placeholder:
        writing_animation.empty()
    st.session_state.history.append(
        Message("ai", llm_response)
    )

st.chat_input(placeholder="Please enter your message here...",on_submit=on_click_callback,key="human_prompt")
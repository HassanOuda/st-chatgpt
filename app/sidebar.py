"""Python file to serve as the st.sidebar of the app"""
import streamlit as st
import llm

def assistant_type():
    if st.session_state.assistant == "General Chatbot":
        st.session_state.model = "chat-bison"
        st.session_state.prompt_template = ""
        st.session_state.temperature = 0.2
        st.session_state.token_limit = 512
        st.session_state.top_p = 0.8
        st.session_state.top_k = 40
        st.session_state.conversation = llm.load_chat(st.session_state.model,st.session_state.temperature,st.session_state.token_limit,st.session_state.top_p,st.session_state.top_k,st.session_state.memory)
    elif st.session_state.assistant == "Text Summarization":
        st.session_state.model = "text-bison"
        st.session_state.prompt_template = "Provide a summary with about two sentences for the following {text}"
        st.session_state.temperature = 0.2
        st.session_state.token_limit = 1024
        st.session_state.top_p = 0.8
        st.session_state.top_k = 40
        st.session_state.conversation = llm.load_llm(st.session_state.model,st.session_state.temperature,st.session_state.token_limit,st.session_state.top_p,st.session_state.top_k,st.session_state.prompt_template)
    elif st.session_state.assistant == "Correct spelling/grammar":
        st.session_state.model = "text-bison"
        st.session_state.prompt_template = "Correct the spelling and grammar of this text: {text}"
        st.session_state.temperature = 0.2
        st.session_state.token_limit = 1024
        st.session_state.top_p = 0.8
        st.session_state.top_k = 40
        st.session_state.conversation = llm.load_llm(st.session_state.model,st.session_state.temperature,st.session_state.token_limit,st.session_state.top_p,st.session_state.top_k,st.session_state.prompt_template)
    elif st.session_state.assistant == "Text Generation":
        st.session_state.model = "text-bison"
        st.session_state.prompt_template = "{question}"
        st.session_state.temperature = 0.7
        st.session_state.token_limit = 1024
        st.session_state.top_p = 0.8
        st.session_state.top_k = 40
        st.session_state.conversation = llm.load_llm(st.session_state.model,st.session_state.temperature,st.session_state.token_limit,st.session_state.top_p,st.session_state.top_k,st.session_state.prompt_template)
    elif st.session_state.assistant == "Code Chatbot":
        st.session_state.model = "codechat-bison"
        st.session_state.prompt_template = ""
        st.session_state.temperature = 0.2
        st.session_state.token_limit = 1024
        st.session_state.top_p = 0.8
        st.session_state.top_k = 40
        st.session_state.conversation = llm.load_chat(st.session_state.model,st.session_state.temperature,st.session_state.token_limit,st.session_state.top_p,st.session_state.top_k,st.session_state.memory)
    elif st.session_state.assistant == "Code Generation":
        st.session_state.model = "code-bison"
        st.session_state.prompt_template = "{question}"
        st.session_state.temperature = 0.2
        st.session_state.token_limit = 1024
        st.session_state.top_p = 0.8
        st.session_state.top_k = 40
        st.session_state.conversation = llm.load_llm(st.session_state.model,st.session_state.temperature,st.session_state.token_limit,st.session_state.top_p,st.session_state.top_k,st.session_state.prompt_template)
    return

def sidebar_setup():
    assistant = st.sidebar.selectbox("**Assistant Type:**", ("General Chatbot","Text Summarization", "Correct spelling/grammar", "Text Generation","Code Chatbot","Code Generation"),on_change=assistant_type, key="assistant")
    settings = st.sidebar.expander("⚙️ **Advanced Settings**")
    with settings:
        temperature_val = st.slider('**Temperature:**', 0.0, 1.0, 0.2,step=0.1,format="%.1f", key="temperature")
        token_limit_val = st.slider('**Token Limit:**', 1, 1024,512, step=1, key="token_limit")
        top_p_val = st.slider('**Top-P:**', 0.0, 1.0, 0.8,step=0.1,format="%.1f", key="top_p")
        top_k_val = st.slider('**Top-K:**', 1, 40,40,step=1, key="top_k")
    clear_button = st.sidebar.button("Clear Conversation", key="clear",type="primary")

    if "prompt_template" not in st.session_state:
        st.session_state.prompt_template = ""
    with settings:
        st.text_area(label="**Context:**",value=st.session_state.prompt_template, key="context_input")
        st.button("Update Context", key="context",on_click=context_update)

    # reset conversation
    if clear_button:
        st.session_state['history'] = []

def context_update():
    st.session_state.prompt_template = st.session_state.context_input
    if "chat" in st.session_state.model:
        st.session_state.conversation = llm.load_chat(st.session_state.model,st.session_state.temperature,st.session_state.token_limit,st.session_state.top_p,st.session_state.top_k,st.session_state.memory)
    else:
        st.session_state.conversation = llm.load_llm(st.session_state.model,st.session_state.temperature,st.session_state.token_limit,st.session_state.top_p,st.session_state.top_k,st.session_state.prompt_template)


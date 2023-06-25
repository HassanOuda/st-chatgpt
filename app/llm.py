"""Python file to serve as the frontend"""
import os
from langchain import PromptTemplate, LLMChain, ConversationChain
from langchain.llms import VertexAI
from langchain.chat_models import ChatVertexAI
from google.cloud import aiplatform
from google.oauth2 import service_account

cred = service_account.Credentials.from_service_account_file(os.getenv("CREDENTIALS"))

aiplatform.init(project=os.getenv("PROJECT_ID"),location="us-central1",credentials=cred)


def load_llm(model, temperature, token_limit, top_p, top_k, prompt_template):
    llm = VertexAI(model_name=model,temperature=temperature,max_output_tokens=token_limit,
                top_k=top_k,top_p=top_p)
    return LLMChain(llm=llm,prompt=PromptTemplate.from_template(prompt_template))

def load_chat(model, temperature, token_limit, top_p, top_k, memory):
    llm = ChatVertexAI(model_name=model,temperature=temperature,max_output_tokens=token_limit,
                    top_k=top_k,top_p=top_p)
    return ConversationChain(llm=llm, memory=memory)


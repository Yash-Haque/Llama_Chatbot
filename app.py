from langchain_community.llms import CTransformers
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

import os
import io
import gradio as gr
import time

custom_prompt_template = """
You are an AI coding assistant and your task is to solve coding problems and return code snippets based on
given user's query. Below is the user's query
Query: {query}
You just return the helpful code and related details.
Helpful code and related details:
"""

def set_custom_prompt():
    prompt = PromptTemplate(
        template = custom_prompt_template,
        input_variables = ['query']
    )
    return prompt

def load_model():
    llm = CTransformers(
        model = 'D:\Visual_Studio\LlamaGradio\codellama-7b-instruct.Q4_0.gguf',
        model_type ='llama',
        max_new_tokens = 1096,
        temperature = 0.2,
        repetition_penalty = 1.13
    )

    return llm

def chain_pipeline():
    llm = load_model()
    qa_prompt = set_custom_prompt()
    qa_chain = LLMChain(
        prompt = qa_prompt,
        llm = llm
    )
    return qa_chain

llmchain = chain_pipeline()

def bot(query):
    llm_response = llmchain.run({'query':query})
    return llm_response

with gr.Blocks(title="Code Llama Demo") as demo:
    gr.Markdown("# Code Llama Demo")
    chatbot = gr.Chatbot([], elem_id='chatbot', height=700)
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        bot_message = bot(message)
        chat_history.append((message, bot_message))
        time.sleep(2)
        return "", chat_history
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch()
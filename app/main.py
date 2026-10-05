import streamlit as st
from typing import Sequence
from pydantic_ai.messages import ModelMessage

from agents.main import agent

st.set_page_config(
    page_title="ZERO",
    page_icon="🤖",
    layout="wide",
)

st.title("Agent Zero")


if "processing" not in st.session_state:
    st.session_state.processing = False

if "message_list" not in st.session_state:
    message_list: Sequence[ModelMessage] = []
    st.session_state.message_list = message_list

for message in st.session_state.message_list:
    with st.chat_message(message.kind):
        st.write(message)

def handle_submit():
    st.session_state.processing = True
    user_prompt = st.session_state.prompt_box
    r = agent.run_sync(
        user_prompt=user_prompt,
        message_history=st.session_state.message_list
    )
    st.session_state.message_list = r.all_messages()
    st.write(r.all_messages) 



st.chat_input(
    placeholder="PROMPT", 
    key="prompt_box",
    on_submit=handle_submit,
    disabled=st.session_state.processing
)

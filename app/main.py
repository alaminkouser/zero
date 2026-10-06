import asyncio
import streamlit as st
from typing import Sequence
from pydantic_ai.messages import ModelMessage, ThinkingPart
from pydantic_ai.result import StreamedRunResult
from pydantic_ai.run import AgentRunResultEvent

from agents.main import agent

st.set_page_config(
    page_title="ZERO",
    page_icon="🤖",
    layout="centered",
)

st.title("Agent Zero")


if "processing" not in st.session_state:
    st.session_state.processing = False

if "message_list" not in st.session_state:
    message_list: Sequence[ModelMessage] = []
    st.session_state.message_list = message_list

if "ssr_list" not in st.session_state:
    ssr_list: list[StreamedRunResult] = []
    st.session_state.ssr_list = ssr_list

for message in st.session_state.message_list:
    avatar = "human"
    if message.kind == "response":
        avatar = "ai"
    with st.chat_message(avatar):
        for part in message.parts:
            if isinstance(part, ThinkingPart):
                st.markdown(part.content)

async def handle_submit_async():
    st.session_state.processing = True
    user_prompt = st.session_state.prompt_box

    try:
        async with agent.run_stream_events(
            user_prompt=user_prompt,
            message_history=st.session_state.message_list,
        ) as events:
            async for event in events:
                if isinstance(event, AgentRunResultEvent):
                    st.session_state.message_list = event.result.all_messages()

    finally:

        st.session_state.processing = False


def handle_submit():
    asyncio.run(handle_submit_async())


st.chat_input(
    placeholder="PROMPT", 
    key="prompt_box",
    on_submit=handle_submit,
    disabled=st.session_state.processing
)

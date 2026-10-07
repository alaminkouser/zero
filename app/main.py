import asyncio
import streamlit as st
from typing import Any, Sequence
from pydantic_ai.messages import ModelMessage, UserPromptPart, ThinkingPart, TextPart, ToolCallPart,  ToolReturnPart
from pydantic_ai.run import AgentRunResultEvent

from agents.main import agent

st.set_page_config(
    page_title="ZERO",
    page_icon="🤖",
    layout="centered",
)

st.title("Agent Zero", text_alignment="center", anchor=False)

if "processing" not in st.session_state:
    st.session_state.processing = False

if "message_list" not in st.session_state:
    message_list: Sequence[ModelMessage] = []
    st.session_state.message_list = message_list

if "event_list" not in st.session_state:
    event_list: Sequence[Any] = []
    st.session_state.event_list = event_list

for message in st.session_state.message_list:
    for part in message.parts:
        avatar = "human"
        if type(part).__name__ != "UserPromptPart":
            avatar = "ai"
        if isinstance(part, UserPromptPart):
            with st.chat_message(avatar):
                st.markdown(part.content)
        elif isinstance(part, ThinkingPart):
            with st.chat_message(avatar):
                st.markdown(part.content)
        elif isinstance(part, TextPart):
            with st.chat_message(avatar):
                st.markdown(part.content)
        elif isinstance(part, ToolCallPart):
            with st.chat_message(avatar):
                st.write(part.tool_name)
                if part.args_as_dict():
                    st.write(part.args_as_dict())
                else:
                    st.write(part)
        elif isinstance(part, ToolReturnPart):
            with st.chat_message(avatar):
                st.write(part.content)
        else:
            st.warning(type(part).__name__)


current_events = st.empty()

async def handle_submit_async():
    st.session_state.processing = True
    user_prompt = st.session_state.prompt_box

    agent_main = agent()

    try:
        async with agent_main.run_stream_events(
            user_prompt=user_prompt,
            message_history=st.session_state.message_list,
        ) as events:
            async for event in events:
                print(event.event_kind)
                current_events.write(event.event_kind)
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

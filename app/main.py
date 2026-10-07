import asyncio
import streamlit as st
from typing import Sequence
from pydantic_ai.messages import (
    ModelMessage,
    RetryPromptPart,
    UserPromptPart,
    ThinkingPart,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
)
from pydantic_ai.run import AgentRunResultEvent

from agents.main import agent

st.set_page_config(
    page_title="ZERO",
    page_icon="🤖",
    layout="centered",
)

st.title("~", text_alignment="center", anchor=False)

if "message_list" not in st.session_state:
    message_list: Sequence[ModelMessage] = []
    st.session_state.message_list = message_list

for message in st.session_state.message_list:
    for part in message.parts:
        avatar = "human"
        if type(part).__name__ != "UserPromptPart":
            avatar = "assistant"
        if isinstance(part, UserPromptPart):
            with st.chat_message(avatar):
                st.markdown(part.content)
        elif isinstance(part, ThinkingPart):
            with st.chat_message(avatar):
                st.markdown(part.content)
        elif isinstance(part, TextPart):
            if part.content.strip() != "":
                with st.chat_message(avatar):
                    st.markdown(part.content.strip())
        elif isinstance(part, ToolCallPart):
            with st.chat_message(avatar):
                if part.args_as_dict():
                    st.write(part.args_as_dict())
                else:
                    st.write(part.tool_name)
                    st.write(part)
        elif isinstance(part, ToolReturnPart):
            with st.chat_message(avatar):
                st.write(part.content)
        elif isinstance(part, RetryPromptPart):
            with st.chat_message(avatar):
                st.markdown(part.content)
        else:
            st.warning(type(part).__name__)

user_prompt_part = st.empty()
current_events = st.empty()

error = st.empty()


async def handle_submit_async():
    user_prompt = st.session_state.prompt_box
    with user_prompt_part.chat_message("human"):
        st.text(user_prompt)

    try:
        agent_main = agent()
        async with agent_main.run_stream_events(
            user_prompt=user_prompt,
            message_history=st.session_state.message_list,
        ) as events:
            async for event in events:
                with current_events.chat_message("assistant"):
                    st.write(event)
                if isinstance(event, AgentRunResultEvent):
                    st.session_state.message_list = event.result.all_messages()

    except Exception as e:
        error.write(e)

    finally:
        user_prompt_part.empty()


def handle_submit():
    asyncio.run(handle_submit_async())


st.chat_input(
    placeholder="PROMPT",
    key="prompt_box",
    on_submit=handle_submit,
    submit_mode="disable",
)

import asyncio
from pydantic_ai import TextPartDelta
import streamlit as st
from typing import Sequence, Literal
from pydantic import BaseModel
from pydantic_ai.messages import (
    ModelMessage,
    RetryPromptPart,
    UserPromptPart,
    ThinkingPart,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    PartStartEvent,
    PartDeltaEvent,
    PartEndEvent,
    ThinkingPartDelta,
    FunctionToolCallEvent,
    FunctionToolResultEvent,
    FinalResultEvent,
)
from pydantic_ai.run import AgentRunResultEvent

from agents.main import agent

st.set_page_config(
    page_title="ZERO",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖", text_alignment="center", anchor=False)

if "message_list" not in st.session_state:
    message_list: Sequence[ModelMessage] = []
    st.session_state.message_list = message_list

for message in st.session_state.message_list:
    for part in message.parts:
        avatar = "human"
        if not isinstance(part, UserPromptPart):
            avatar = "assistant"

        if isinstance(part, UserPromptPart):
            with st.chat_message(avatar):
                st.markdown(part.content, anchors=False)
        elif isinstance(part, ThinkingPart):
            with st.chat_message(avatar):
                st.markdown(part.content, anchors=False)
        elif isinstance(part, TextPart):
            if part.content.strip() != "":
                with st.chat_message(avatar):
                    st.markdown(part.content.strip(), anchors=False)
        elif isinstance(part, ToolCallPart):
            with st.chat_message(avatar):
                if part.args_as_dict():
                    st.write(part.args_as_dict())
                else:
                    st.write(part.tool_name)
                    st.write(part)
        elif isinstance(part, ToolReturnPart):
            with st.chat_message(avatar):
                with st.expander(part.tool_name):
                    st.write(part.content)
        elif isinstance(part, RetryPromptPart):
            with st.chat_message(avatar):
                st.markdown(part.content, anchors=False)
        else:
            st.warning("E:MESSAGE_LIST:MESSAGE:PART\n\n" + type(part).__name__)


user_prompt_part = st.empty()
current_events = st.empty()
processing = st.empty()

error = st.empty()


class StreamingContent(BaseModel):
    type: Literal[
        "THINKING", "TEXT", "FUNCTION_TOOL_CALL_EVENT", "FUNCTION_TOOL_RESULT_EVENT", ""
    ] = ""
    content: str = ""
    function_tool_call_event: FunctionToolCallEvent | None = None
    function_tool_result_event: FunctionToolResultEvent | None = None


def current_events_show(
    event_list: list[
        PartStartEvent
        | PartDeltaEvent
        | PartEndEvent
        | FunctionToolCallEvent
        | FunctionToolResultEvent
        | FinalResultEvent
    ],
):
    streaming_content: list[StreamingContent] = []
    for event in event_list:
        if isinstance(event, FunctionToolCallEvent):
            current_stream = StreamingContent()
            streaming_content.append(current_stream)
            current_stream.type = "FUNCTION_TOOL_CALL_EVENT"
            current_stream.function_tool_call_event = event

        if isinstance(event, FunctionToolResultEvent):
            current_stream = StreamingContent()
            streaming_content.append(current_stream)
            current_stream.type = "FUNCTION_TOOL_RESULT_EVENT"
            current_stream.function_tool_result_event = event

        if isinstance(event, PartStartEvent):

            if isinstance(event.part, (ThinkingPart, TextPart)):
                current_stream = StreamingContent()
                streaming_content.append(current_stream)
                current_stream.type = "THINKING"
                if isinstance(event.part, TextPart):
                    current_stream.type = "TEXT"
                current_stream.content = event.part.content

        if isinstance(event, PartDeltaEvent):

            if isinstance(event.delta, (ThinkingPartDelta, TextPartDelta)):
                streaming_content[-1].content += event.delta.content_delta or ""

        if isinstance(event, PartEndEvent):

            if isinstance(event.part, (ThinkingPart, TextPart)):
                streaming_content[-1].content = event.part.content

    with current_events.container():
        for item in streaming_content:
            if (
                item.type == "FUNCTION_TOOL_CALL_EVENT"
                and item.function_tool_call_event != None
            ):
                with st.chat_message("assistant"):
                    st.write(item.function_tool_call_event.part.args)

            if (
                item.type == "FUNCTION_TOOL_RESULT_EVENT"
                and item.function_tool_result_event != None
            ):
                with st.chat_message("assistant"):
                    st.write(item.function_tool_result_event.part.content)
            if item.type == "THINKING":
                with st.chat_message("assistant"):
                    st.markdown(item.content, anchors=False)
            if item.type == "TEXT":
                if item.content.strip() != "":
                    with st.chat_message("assistant"):
                        st.markdown(item.content.strip(), anchors=False)


async def handle_submit_async():
    user_prompt = st.session_state.prompt_box
    with user_prompt_part.chat_message("human"):
        st.text(user_prompt)

    try:
        agent_main = agent()
        async with agent_main.run_stream_events(
            user_prompt=user_prompt,
            message_history=st.session_state.message_list,
            retries=10,
        ) as events:
            current_event_list: list[
                PartStartEvent
                | PartDeltaEvent
                | PartEndEvent
                | FunctionToolCallEvent
                | FunctionToolResultEvent
                | FinalResultEvent
            ] = []
            async for event in events:
                if isinstance(
                    event,
                    (
                        PartStartEvent,
                        PartDeltaEvent,
                        PartEndEvent,
                        FunctionToolCallEvent,
                        FunctionToolResultEvent,
                        FinalResultEvent,
                    ),
                ):
                    current_event_list.append(event)
                    current_events_show(current_event_list)

                if isinstance(event, AgentRunResultEvent):
                    st.session_state.message_list = event.result.all_messages()

    except Exception as e:
        error.write(e)

    finally:
        user_prompt_part.empty()


def handle_submit():
    with processing.spinner(text="", show_time=True):
        asyncio.run(handle_submit_async())


st.chat_input(
    placeholder="PROMPT",
    key="prompt_box",
    on_submit=handle_submit,
    submit_mode="disable",
)

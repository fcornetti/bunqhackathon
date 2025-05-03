import agent_tools
import streamlit as st


st.markdown(
    """
    <style>
        html, body, [class*="css"]  {
            font-family: 'Comic Sans MS', cursive, sans-serif;
        }
    </style>
""",
    unsafe_allow_html=True,
)


col1, col2 = st.columns([10, 2])

with col1:
    st.title("Blink - bunq Agentic Chatbot")

with col2:
    st.image("./ui/blink_logo_black.png", caption="", width=100)


st.sidebar.markdown(
    """This app shows an Agentic Chatbot powered using Amazon Bedrock Agents to answer questions and execute actions to empower **bunq** user."""
)
clear_button = st.sidebar.button("Clear Conversation", key="clear")
# reset sessions state on clear
if clear_button:
    st.session_state.messages = []
    st.session_state.session_id = agent_tools.generate_random_15digit()


if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.session_id = agent_tools.generate_random_15digit()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "traces" in message:
            trace_container = st.container()
            for trace in message["traces"]:
                with trace_container.expander(trace["trace_type"]):
                    if trace["trace_type"] == "codeInterpreter":
                        st.code(trace["text"], language="python")
                    else:
                        st.markdown(trace["text"])

        st.markdown(message["content"][0]["text"])
        # TODO build for show images

if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": [{"text": prompt}]})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        trace_container = st.container()

        result = agent_tools.invoke_bedrock_agent(
            prompt, st.session_state.session_id, trace_container
        )

        message_placeholder.markdown(result["text"])

        # TODO add code for show images

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": [{"text": f"{full_response}"}],
            "images": result["images"],
            "traces": result["traces"],
        }
    )

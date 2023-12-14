from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os
import shelve
import uuid

load_dotenv()

st.title("ChatGPT-like Chatbot Demo")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("styles.css")


def load_messages(session_uuid):
    with shelve.open("chat_history") as db:
        return db.get(f"messages_{session_uuid}", [])


def save_messages(session_uuid, messages):
    with shelve.open("chat_history") as db:
        db[f"messages_{session_uuid}"] = messages


def delete_all_sessions():
    with shelve.open("chat_history") as db:
        db.clear()


def get_all_session_uuids():
    with shelve.open("chat_history") as db:
        return list(db.keys())


def create_new_session():
    new_uuid = str(uuid.uuid4())
    st.session_state["session_uuid"] = new_uuid
    st.session_state["messages"] = []
    save_messages(new_uuid, [])
    return new_uuid


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Sidebar
st.sidebar.markdown("### Description\nWelcome to our Generative AI demo.")

# Initialize or load sessions
all_sessions = get_all_session_uuids()

# Default load the last session or create a new one if the DB is empty
if (
    "session_uuid" not in st.session_state
    or st.session_state["session_uuid"] not in all_sessions
):
    if all_sessions:
        st.session_state["session_uuid"] = all_sessions[-1]
    else:
        st.session_state["session_uuid"] = create_new_session()
    st.session_state["messages"] = load_messages(st.session_state["session_uuid"])

# Session Selector
selected_session = st.sidebar.selectbox(
    "Select a session:", all_sessions, format_func=lambda x: x.split("_")[-1]
)

if selected_session and selected_session != st.session_state["session_uuid"]:
    st.session_state["session_uuid"] = selected_session
    st.session_state["messages"] = load_messages(selected_session)

if st.sidebar.button("Start New Session"):
    create_new_session()
    all_sessions = get_all_session_uuids()  # Update the session list
    st.rerun()  # Rerun to refresh the selectbox

if st.sidebar.button("Delete All Sessions"):
    delete_all_sessions()
    st.sidebar.success("All sessions deleted!")
    st.rerun()  # Rerun to update the UI

# Main chat interface
for message in st.session_state.get("messages", []):
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state["messages"],
            stream=True,
        ):
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_messages(st.session_state["session_uuid"], st.session_state["messages"])

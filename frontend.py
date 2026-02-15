# import streamlit as st
# from backend import (
#     chatbot,
#     retrieve_user_threads,
#     add_thread_for_user,
#     login_user,
#     register_user,
#     verify_token,
# )
# from langchain_core.messages import HumanMessage
# import uuid

# # ---------------- AUTH CHECK ----------------
# if "token" in st.session_state:
#     username = verify_token(st.session_state["token"])
#     if username:
#         st.session_state.logged_in = True
#         st.session_state.username = username
#     else:
#         st.session_state.clear()

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# # ---------------- LOGIN / SIGNUP ----------------
# if not st.session_state.logged_in:

#     st.title("LangGraph Chatbot")

#     mode = st.radio("Mode", ["Login", "Sign Up"])
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if mode == "Login":
#         if st.button("Login"):
#             token = login_user(username, password)
#             if token:
#                 st.session_state.token = token
#                 st.session_state.logged_in = True
#                 st.session_state.username = username
#                 st.rerun()
#             else:
#                 st.error("Invalid credentials")

#     else:
#         if st.button("Create Account"):
#             if register_user(username, password):
#                 st.success("Account created. Please login.")
#             else:
#                 st.error("Username exists")

#     st.stop()

# # ---------------- UTILITIES ----------------
# def generate_thread_id():
#     return str(uuid.uuid4())

# def reset_chat():
#     st.session_state["thread_id"] = generate_thread_id()
#     st.session_state["message_history"] = []
#     if "thread_initialized" in st.session_state:
#         del st.session_state["thread_initialized"]

# def load_conversation(thread_id):
#     state = chatbot.get_state(
#         config={"configurable": {"thread_id": thread_id}}
#     )
#     return state.values.get("messages", [])

# # ---------------- SESSION SETUP ----------------
# if "thread_id" not in st.session_state:
#     st.session_state["thread_id"] = generate_thread_id()

# if "message_history" not in st.session_state:
#     st.session_state["message_history"] = []

# if "chat_threads" not in st.session_state:
#     st.session_state["chat_threads"] = retrieve_user_threads(
#         st.session_state.username
#     )

# # ---------------- SIDEBAR ----------------
# st.sidebar.title(f"Welcome {st.session_state.username}")

# if st.sidebar.button("Logout"):
#     st.session_state.clear()
#     st.rerun()

# if st.sidebar.button("New Chat"):
#     reset_chat()

# st.sidebar.header("My Conversations")

# for thread_id, title in st.session_state["chat_threads"][::-1]:
#     if st.sidebar.button(title):
#         st.session_state["thread_id"] = thread_id
#         messages = load_conversation(thread_id)

#         temp = []
#         for msg in messages:
#             role = "assistant"
#             if isinstance(msg, HumanMessage):
#                 role = "user"
#             temp.append({"role": role, "content": msg.content})

#         st.session_state["message_history"] = temp
#         st.session_state["thread_initialized"] = True

# # ---------------- CHAT UI ----------------
# for message in st.session_state["message_history"]:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# user_input = st.chat_input("Type here")

# if user_input:

#     if "thread_initialized" not in st.session_state:
#         add_thread_for_user(
#             st.session_state.username,
#             st.session_state["thread_id"],
#             user_input,
#         )
#         st.session_state["thread_initialized"] = True
#         st.session_state["chat_threads"] = retrieve_user_threads(
#             st.session_state.username
#         )

#     st.session_state["message_history"].append(
#         {"role": "user", "content": user_input}
#     )

#     with st.chat_message("assistant"):
#         ai_message = st.write_stream(
#             chunk.content
#             for chunk, _ in chatbot.stream(
#                 {"messages": [HumanMessage(content=user_input)]},
#                 config={
#                     "configurable": {
#                         "thread_id": st.session_state["thread_id"]
#                     }
#                 },
#                 stream_mode="messages",
#             )
#         )

#     st.session_state["message_history"].append(
#         {"role": "assistant", "content": ai_message}
#     )



import streamlit as st
from backend import (
    chatbot,
    retrieve_user_threads,
    add_thread_for_user,
    login_user,
    register_user,
    reset_password,
    verify_token,
)
from langchain_core.messages import HumanMessage
import uuid

# ---------------- AUTH CHECK ----------------
if "token" in st.session_state:
    username = verify_token(st.session_state["token"])
    if username:
        st.session_state.logged_in = True
        st.session_state.username = username
    else:
        st.session_state.clear()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- AUTH SCREEN ----------------
if not st.session_state.logged_in:

    st.title("LangGraph Chatbot")

    # Styling for buttons
    st.markdown("""
    <style>
    button[kind="secondary"] {
        border-radius: 10px;
        height: 3em;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("### Choose an option")

    col1, col2, col3 = st.columns(3)

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "Login"

    with col1:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state.auth_mode = "Login"

    with col2:
        if st.button("📝 Sign Up", use_container_width=True):
            st.session_state.auth_mode = "Sign Up"

    with col3:
        if st.button("♻️ Reset", use_container_width=True):
            st.session_state.auth_mode = "Reset Password"

    mode = st.session_state.auth_mode

    st.divider()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if mode == "Login":
        if st.button("Login"):
            token = login_user(username, password)
            if token:
                st.session_state.token = token
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    elif mode == "Sign Up":
        security_answer = st.text_input("Security Answer (favorite color?)")

        if st.button("Create Account"):
            if register_user(username, password, security_answer):
                st.success("Account created. Please login.")
            else:
                st.error("Username exists")

    else:
        security_answer = st.text_input("Security Answer")
        new_password = st.text_input("New Password", type="password")

        if st.button("Reset Password"):
            if reset_password(username, security_answer, new_password):
                st.success("Password updated. Please login.")
            else:
                st.error("Invalid username or answer")

    st.stop()

# ---------------- UTILITIES ----------------
def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    st.session_state["thread_id"] = generate_thread_id()
    st.session_state["message_history"] = []
    if "thread_initialized" in st.session_state:
        del st.session_state["thread_initialized"]

def load_conversation(thread_id):
    state = chatbot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )
    return state.values.get("messages", [])

# ---------------- SESSION SETUP ----------------
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_user_threads(
        st.session_state.username
    )

# ---------------- SIDEBAR ----------------
st.sidebar.title(f"Welcome {st.session_state.username}")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")

for thread_id, title in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(title):
        st.session_state["thread_id"] = thread_id
        messages = load_conversation(thread_id)

        temp = []
        for msg in messages:
            role = "assistant"
            if isinstance(msg, HumanMessage):
                role = "user"
            temp.append({"role": role, "content": msg.content})

        st.session_state["message_history"] = temp
        st.session_state["thread_initialized"] = True

# ---------------- CHAT UI ----------------
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type here")

if user_input:

    if "thread_initialized" not in st.session_state:
        add_thread_for_user(
            st.session_state.username,
            st.session_state["thread_id"],
            user_input,
        )
        st.session_state["thread_initialized"] = True
        st.session_state["chat_threads"] = retrieve_user_threads(
            st.session_state.username
        )

    st.session_state["message_history"].append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            chunk.content
            for chunk, _ in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config={"configurable": {"thread_id": st.session_state["thread_id"]}},
                stream_mode="messages",
            )
        )

    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )

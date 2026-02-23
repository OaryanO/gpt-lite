# from langgraph.graph import StateGraph, START, END
# from typing import TypedDict, Annotated
# from langchain_core.messages import BaseMessage
# from langchain_groq import ChatGroq
# from langgraph.checkpoint.sqlite import SqliteSaver
# from langgraph.graph.message import add_messages
# from dotenv import load_dotenv
# import sqlite3
# import bcrypt
# import jwt
# import datetime
# import os
# import psycopg2

# load_dotenv()

# SECRET_KEY = os.getenv("JWT_SECRET")
# DATABASE_URL = os.getenv("DATABASE_URL")

# llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# # ---------------- SQLITE MEMORY ----------------
# memory_conn = sqlite3.connect("memory.db", check_same_thread=False)
# checkpointer = SqliteSaver(conn=memory_conn)

# # ---------------- POSTGRES ----------------
# pg_conn = psycopg2.connect(DATABASE_URL)
# pg_cursor = pg_conn.cursor()

# pg_cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     username TEXT PRIMARY KEY,
#     password BYTEA,
#     security_answer TEXT
# )
# """)

# pg_cursor.execute("""
# CREATE TABLE IF NOT EXISTS user_threads (
#     username TEXT,
#     thread_id TEXT,
#     title TEXT
# )
# """)

# pg_conn.commit()

# # ---------------- STATE ----------------
# class ChatState(TypedDict):
#     messages: Annotated[list[BaseMessage], add_messages]

# def chat_node(state: ChatState):
#     response = llm.invoke(state["messages"])
#     return {"messages": [response]}

# def generate_thread_title(first_message):
#     prompt = f"Create a short 3-5 word title for this chat:\n{first_message}"
#     response = llm.invoke(prompt)
#     return response.content.strip()

# # ---------------- GRAPH ----------------
# graph = StateGraph(ChatState)
# graph.add_node("chat_node", chat_node)
# graph.add_edge(START, "chat_node")
# graph.add_edge("chat_node", END)

# chatbot = graph.compile(checkpointer=checkpointer)

# # ---------------- JWT ----------------
# def create_token(username):
#     payload = {
#         "username": username,
#         "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12),
#     }
#     return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# def verify_token(token):
#     try:
#         decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         return decoded["username"]
#     except:
#         return None

# # ---------------- AUTH ----------------
# def register_user(username, password, security_answer):
#     try:
#         hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
#         normalized_answer = security_answer.strip().lower()

#         pg_cursor.execute(
#             "INSERT INTO users (username, password, security_answer) VALUES (%s, %s, %s)",
#             (username, hashed, normalized_answer),
#         )
#         pg_conn.commit()
#         return True
#     except:
#         pg_conn.rollback()
#         return False

# def login_user(username, password):
#     pg_cursor.execute(
#         "SELECT password FROM users WHERE username=%s",
#         (username,),
#     )
#     row = pg_cursor.fetchone()

#     if not row:
#         return None

#     stored_hash = bytes(row[0])

#     if bcrypt.checkpw(password.encode(), stored_hash):
#         return create_token(username)

#     return None

# def reset_password(username, security_answer, new_password):
#     pg_cursor.execute(
#         "SELECT security_answer FROM users WHERE username=%s",
#         (username,),
#     )
#     row = pg_cursor.fetchone()

#     if not row:
#         return False

#     if row[0] != security_answer.strip().lower():
#         return False

#     new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())

#     pg_cursor.execute(
#         "UPDATE users SET password=%s WHERE username=%s",
#         (new_hash, username),
#     )
#     pg_conn.commit()

#     return True

# # ---------------- THREADS ----------------
# def add_thread_for_user(username, thread_id, first_message):
#     title = generate_thread_title(first_message)
#     pg_cursor.execute(
#         "INSERT INTO user_threads (username, thread_id, title) VALUES (%s, %s, %s)",
#         (username, str(thread_id), title),
#     )
#     pg_conn.commit()

# def retrieve_user_threads(username):
#     pg_cursor.execute(
#         "SELECT thread_id, title FROM user_threads WHERE username=%s",
#         (username,),
#     )
#     return pg_cursor.fetchall()


# _______________________________________________________________________________________________________
# from langgraph.graph import StateGraph, START, END
# from typing import TypedDict, Annotated
# from langchain_core.messages import BaseMessage
# from langchain_groq import ChatGroq
# from langgraph.checkpoint.sqlite import SqliteSaver
# from langgraph.graph.message import add_messages
# from dotenv import load_dotenv
# import sqlite3
# import bcrypt
# import jwt
# import datetime
# import os
# import psycopg2

# load_dotenv()

# SECRET_KEY = os.getenv("JWT_SECRET")
# DATABASE_URL = os.getenv("DATABASE_URL")

# llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# memory_conn = sqlite3.connect("memory.db", check_same_thread=False)
# checkpointer = SqliteSaver(conn=memory_conn)

# pg_conn = psycopg2.connect(DATABASE_URL)
# pg_cursor = pg_conn.cursor()

# pg_cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     username TEXT PRIMARY KEY,
#     password BYTEA,
#     security_answer TEXT
# )
# """)

# pg_cursor.execute("""
# CREATE TABLE IF NOT EXISTS user_threads (
#     username TEXT,
#     thread_id TEXT PRIMARY KEY,
#     title TEXT
# )
# """)

# pg_conn.commit()

# class ChatState(TypedDict):
#     messages: Annotated[list[BaseMessage], add_messages]

# def chat_node(state: ChatState):
#     response = llm.invoke(state["messages"])
#     return {"messages": [response]}

# def generate_thread_title(first_message):
#     prompt = f"Create a short 3-5 word title for this chat:\n{first_message}"
#     response = llm.invoke(prompt)
#     return response.content.strip()

# graph = StateGraph(ChatState)
# graph.add_node("chat_node", chat_node)
# graph.add_edge(START, "chat_node")
# graph.add_edge("chat_node", END)

# chatbot = graph.compile(checkpointer=checkpointer)

# def create_token(username):
#     payload = {
#         "username": username,
#         "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12),
#     }
#     return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# def verify_token(token):
#     try:
#         decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         return decoded["username"]
#     except:
#         return None

# def register_user(username, password, security_answer):
#     try:
#         hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
#         normalized_answer = security_answer.strip().lower()

#         pg_cursor.execute(
#             "INSERT INTO users (username, password, security_answer) VALUES (%s, %s, %s)",
#             (username, hashed, normalized_answer),
#         )
#         pg_conn.commit()
#         return True
#     except:
#         pg_conn.rollback()
#         return False

# def login_user(username, password):
#     pg_cursor.execute(
#         "SELECT password FROM users WHERE username=%s",
#         (username,),
#     )
#     row = pg_cursor.fetchone()

#     if not row:
#         return None

#     stored_hash = bytes(row[0])
#     if bcrypt.checkpw(password.encode(), stored_hash):
#         return create_token(username)

#     return None

# def reset_password(username, security_answer, new_password):
#     pg_cursor.execute(
#         "SELECT security_answer FROM users WHERE username=%s",
#         (username,),
#     )
#     row = pg_cursor.fetchone()

#     if not row:
#         return False

#     if row[0] != security_answer.strip().lower():
#         return False

#     new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())

#     pg_cursor.execute(
#         "UPDATE users SET password=%s WHERE username=%s",
#         (new_hash, username),
#     )
#     pg_conn.commit()
#     return True

# def add_thread_for_user(username, thread_id, first_message):
#     title = generate_thread_title(first_message)
#     pg_cursor.execute(
#         "INSERT INTO user_threads (username, thread_id, title) VALUES (%s, %s, %s)",
#         (username, str(thread_id), title),
#     )
#     pg_conn.commit()

# def retrieve_user_threads(username):
#     pg_cursor.execute(
#         "SELECT thread_id, title FROM user_threads WHERE username=%s",
#         (username,),
#     )
#     return pg_cursor.fetchall()

# def delete_thread(username, thread_id):
#     pg_cursor.execute(
#         "DELETE FROM user_threads WHERE username=%s AND thread_id=%s",
#         (username, thread_id),
#     )
#     pg_conn.commit()

# def rename_thread(username, thread_id, new_title):
#     pg_cursor.execute(
#         "UPDATE user_threads SET title=%s WHERE username=%s AND thread_id=%s",
#         (new_title.strip(), username, thread_id),
#     )
#     pg_conn.commit()





# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
# from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import bcrypt
import jwt
import datetime
import os
import psycopg



# ---------------- ENV ----------------
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")

if not SECRET_KEY:
    raise ValueError("JWT_SECRET not set")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set")

# ---------------- LLM ----------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# ---------------- LANGGRAPH POSTGRES CHECKPOINTER ----------------
# IMPORTANT: Correct initialization for latest LangGraph versions
# from langgraph.checkpoint.postgres import PostgresSaver
import os
os.environ["PGOPTIONS"] = "-c prepare_threshold=0"

from langgraph.checkpoint.postgres import PostgresSaver

# # Create context manager
# _postgres_cm = PostgresSaver.from_conn_string(DATABASE_URL)

# # Enter context manager to get real saver
# checkpointer = _postgres_cm.__enter__()

# # Now this is a real saver instance
# checkpointer.setup()


# from langgraph.checkpoint.postgres import PostgresSaver

_postgres_cm = PostgresSaver.from_conn_string(
    DATABASE_URL
)
checkpointer = _postgres_cm.__enter__()
checkpointer.setup()
# ---------------- POSTGRES CONNECTION (AUTH + THREADS) ----------------
# pg_conn = psycopg.connect(DATABASE_URL)
# pg_cursor = pg_conn.cursor()
pg_conn = psycopg.connect(
    DATABASE_URL # disable server-side prepared statements
)
pg_cursor = pg_conn.cursor()

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password BYTEA,
    security_answer TEXT
)
""")

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS user_threads (
    username TEXT,
    thread_id TEXT PRIMARY KEY,
    title TEXT
)
""")

pg_conn.commit()

# ---------------- STATE ----------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# ---------------- CHAT NODE ----------------
def chat_node(state: ChatState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# ---------------- GRAPH ----------------
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

# ---------------- JWT ----------------
def create_token(username: str):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["username"]
    except Exception:
        return None

# ---------------- AUTH ----------------
def register_user(username: str, password: str, security_answer: str):
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        normalized_answer = security_answer.strip().lower()

        pg_cursor.execute(
            "INSERT INTO users (username, password, security_answer) VALUES (%s, %s, %s)",
            (username, hashed, normalized_answer),
        )
        pg_conn.commit()
        return True
    except Exception:
        pg_conn.rollback()
        return False

def login_user(username: str, password: str):
    pg_cursor.execute(
        "SELECT password FROM users WHERE username=%s",
        (username,),
    )
    row = pg_cursor.fetchone()

    if not row:
        return None

    stored_hash = bytes(row[0])

    if bcrypt.checkpw(password.encode(), stored_hash):
        return create_token(username)

    return None

def reset_password(username: str, security_answer: str, new_password: str):
    pg_cursor.execute(
        "SELECT security_answer FROM users WHERE username=%s",
        (username,),
    )
    row = pg_cursor.fetchone()

    if not row:
        return False

    if row[0] != security_answer.strip().lower():
        return False

    new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())

    pg_cursor.execute(
        "UPDATE users SET password=%s WHERE username=%s",
        (new_hash, username),
    )
    pg_conn.commit()

    return True

# ---------------- THREAD MANAGEMENT ----------------
def generate_thread_title(first_message: str):
    prompt = f"Create a short 3-5 word title for this conversation:\n{first_message}"
    response = llm.invoke(prompt)
    return response.content.strip()

def add_thread_for_user(username: str, thread_id: str, first_message: str):
    title = generate_thread_title(first_message)

    pg_cursor.execute(
        "INSERT INTO user_threads (username, thread_id, title) VALUES (%s, %s, %s)",
        (username, str(thread_id), title),
    )
    pg_conn.commit()

def retrieve_user_threads(username: str):
    pg_cursor.execute(
        "SELECT thread_id, title FROM user_threads WHERE username=%s",
        (username,),
    )
    return pg_cursor.fetchall()

def delete_thread(username: str, thread_id: str):
    pg_cursor.execute(
        "DELETE FROM user_threads WHERE username=%s AND thread_id=%s",
        (username, thread_id),
    )
    pg_conn.commit()

def rename_thread(username: str, thread_id: str, new_title: str):
    pg_cursor.execute(
        "UPDATE user_threads SET title=%s WHERE username=%s AND thread_id=%s",
        (new_title.strip(), username, thread_id),
    )
    pg_conn.commit()

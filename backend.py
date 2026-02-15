from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3
import bcrypt
import jwt
import datetime
import os
import psycopg2

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")

# ---------------- LLM ----------------
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# ---------------- SQLITE (LangGraph memory) ----------------
memory_conn = sqlite3.connect("memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=memory_conn)

# ---------------- POSTGRES (Supabase) ----------------
pg_conn = psycopg2.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password BYTEA
)
""")

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS user_threads (
    username TEXT,
    thread_id TEXT,
    title TEXT
)
""")

pg_conn.commit()

# ---------------- STATE ----------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def generate_thread_title(first_message):
    prompt = f"Create a short 3-5 word title for this chat:\n{first_message}"
    response = llm.invoke(prompt)
    return response.content.strip()

# ---------------- GRAPH ----------------
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

# ---------------- JWT ----------------
def create_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["username"]
    except:
        return None

# ---------------- AUTH ----------------
def register_user(username, password):
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        pg_cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed),
        )
        pg_conn.commit()
        return True
    except:
        pg_conn.rollback()
        return False

def login_user(username, password):
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

# ---------------- THREAD MANAGEMENT ----------------
def add_thread_for_user(username, thread_id, first_message):
    title = generate_thread_title(first_message)
    pg_cursor.execute(
        "INSERT INTO user_threads (username, thread_id, title) VALUES (%s, %s, %s)",
        (username, str(thread_id), title),
    )
    pg_conn.commit()

def retrieve_user_threads(username):
    pg_cursor.execute(
        "SELECT thread_id, title FROM user_threads WHERE username=%s",
        (username,),
    )
    return pg_cursor.fetchall()

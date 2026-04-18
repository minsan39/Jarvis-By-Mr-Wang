import os
import json

DATA_DIR = "data"

def load_session(sessions_file)-> dict:
    if os.path.exists(sessions_file):
        with open(sessions_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return None

def new_session(messages: list)-> None:
    messages.clear()

def delete_session(time_str: str)-> None:
    filepath = os.path.join(DATA_DIR, f"{time_str}.json")
    if os.path.exists(filepath):
        os.remove(filepath)

def save_session(session: dict, messages: list)-> None:
    if messages==[]:
        return
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{session['time']}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({
            "content": session.get("content", ""),
            "time": session["time"],
            "messages": messages
        }, f, indent=4, ensure_ascii=False)

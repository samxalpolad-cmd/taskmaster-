import sqlite3
import json
from datetime import datetime

# ------------------------------------------------
# DATABASE SETUP
# ------------------------------------------------

def init_db():
    conn = sqlite3.connect('taskmaster.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            title     TEXT,
            status    TEXT DEFAULT 'pending',
            created   TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT,
            message  TEXT,
            time     TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("[DB] Database initialized: taskmaster.db")

# ------------------------------------------------
# TASKS CRUD
# ------------------------------------------------

def add_task(title):
    conn = sqlite3.connect('taskmaster.db')
    cursor = conn.cursor()
    created = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute('INSERT INTO tasks (title, status, created) VALUES (?, ?, ?)', (title, 'pending', created))
    conn.commit()
    conn.close()
    print(f"[POST] Task added: {title}")

def get_all_tasks():
    conn = sqlite3.connect('taskmaster.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    conn.close()
    tasks = [{"id": r[0], "title": r[1], "status": r[2], "created": r[3]} for r in rows]
    print("\n[GET] All Tasks (JSON):")
    print(json.dumps(tasks, indent=4))
    return tasks

def update_task(task_id, new_title):
    conn = sqlite3.connect('taskmaster.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET title = ? WHERE id = ?', (new_title, task_id))
    conn.commit()
    conn.close()
    print(f"[UPDATE] Task ID {task_id} updated to: {new_title}")

def delete_task(task_id):
    conn = sqlite3.connect('taskmaster.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    print(f"[DELETE] Task ID {task_id} deleted.")

# ------------------------------------------------
# POSTS CRUD
# ------------------------------------------------

def add_post(name, message):
    conn = sqlite3.connect('taskmaster.db')
    cursor = conn.cursor()
    time = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute('INSERT INTO posts (name, message, time) VALUES (?, ?, ?)', (name, message, time))
    conn.commit()
    conn.close()
    print(f"[POST] Forum post added by: {name}")

def get_all_posts():
    conn = sqlite3.connect('taskmaster.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts')
    rows = cursor.fetchall()
    conn.close()
    posts = [{"id": r[0], "name": r[1], "message": r[2], "time": r[3]} for r in rows]
    print("\n[GET] All Forum Posts (JSON):")
    print(json.dumps(posts, indent=4))
    return posts

def delete_post(post_id):
    conn = sqlite3.connect('taskmaster.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    print(f"[DELETE] Post ID {post_id} deleted.")

# ------------------------------------------------
# JSON CONFIG
# ------------------------------------------------

def read_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    print("\n[CONFIG] Current Settings:")
    print(json.dumps(config, indent=4))
    return config

def update_config(key, value):
    with open('config.json', 'r') as f:
        config = json.load(f)
    config[key] = value
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
    print(f"[CONFIG] '{key}' updated to '{value}'")

# ------------------------------------------------
# MAIN
# ------------------------------------------------

if __name__ == "__main__":
    init_db()
    print("\n=== Task Master - Database System ===\n")
# TASKS
    add_task("Study: Learn Node.js")
    add_task("Write code: Build Task Master")
    add_task("Exercise: Stay healthy")

    get_all_tasks()

    update_task(1, "Study: Learn Node.js and Express (Updated)")
    delete_task(2)

    print("\n[After Update & Delete - Tasks]")
    get_all_tasks()

    # POSTS
    add_post("Samxal", "Task Master is very useful!")
    add_post("Alice", "Pomodoro technique really works!")

    get_all_posts()

    delete_post(1)

    print("\n[After Delete - Posts]")
    get_all_posts()

    # CONFIG
    read_config()
    update_config("theme", "light")
    update_config("language", "az")
    read_config()


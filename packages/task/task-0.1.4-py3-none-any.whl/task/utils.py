import sqlite3
import os
from typing import Tuple, List
from pathlib import Path

database = 'task.db'


def does_db_exist() -> Tuple[bool, bool]:
    """Check if database exists."""
    global database
    prod_path = f"{os.getenv('HOME')}/.task.db"

    if Path('task.db').exists():
        db = True
        is_prod = False
    elif Path(prod_path).exists():
        db, is_prod = True, True
        database = prod_path
    else:
        db, is_prod = False, False
    return db, is_prod


def create_db():
    """Create SQlite3 database."""
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE todo (
                 id INTEGER PRIMARY KEY,
                 project TEXT,
                 task TEXT NOT NULL,
                 urgency INT NOT NULL,
                 due DATE,
                 done BOOLEAN DEFAULT FALSE,
                 datetime TEXT NOT NULL)
        """
    )
    conn.commit()
    conn.close()


def insert_to_db(task_data: dict):
    """Insert task into DB."""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    for data in task_data:
        if task_data[data] is None:
            task_data[data] = ""

    # if task_data['due'] != "":
    #     due = handle_due(task_data['due'])
    # else:
    #     due = task_data['due']

    if task_data['urgency'] == "":
        task_data['urgency'] = 0

    query = "INSERT INTO todo (project, task, urgency, due, datetime) \
             VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')" \
             .format(task_data['project'], task_data['task'],
                     task_data['urgency'], task_data['due'],
                     task_data['datetime'])
    print(query)
    cursor.execute(query)
    conn.commit()
    conn.close()


def list_all_tasks() -> List:
    """Select all tasks."""
    task_list = list()
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    query = "SELECT id, project, task, urgency, due, datetime \
             FROM todo WHERE done = False ORDER by id"
    out = cursor.execute(query)
    for task in out:
        task_list.append(task)
    return task_list


def remove_entry(task_id: int):
    """Remove row."""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    query = f"DELETE FROM todo WHERE id={task_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()


def set_task_done(task_id: int = 0, project: str = None):
    """Set task to done."""
    # TODO : if 0 move latest task
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    if task_id == 0:
        query = "UPDATE TODO SET done = True WHERE id > 0"
    else:
        query = f"UPDATE TODO SET done = True WHERE id={task_id}"

    cursor.execute(query)
    conn.commit()
    conn.close()

    return task_id

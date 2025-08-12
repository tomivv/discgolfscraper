import datetime
import logging
import sqlite3
from typing import List

from models.classes import Course

logger = logging.getLogger(__name__)
connection = sqlite3.connect('database.db')

def init_database() -> None:
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, name TEXT UNIQUE, metrix_id INTEGER, layout_ids TEXT, events TEXT, updated_at datetime)')
    connection.commit()
    cursor.close()

def get_course(name: str) -> Course | None:
    cursor = connection.cursor()
    logger.info(f'EXECUTED: SELECT * FROM courses WHERE name = {name}')
    rows = cursor.execute('SELECT * FROM courses WHERE name = ?', [name]).fetchone()
    cursor.close()
    return rows

def get_course_names() -> List[str]:
    cursor = connection.cursor()
    rows = cursor.execute('SELECT name FROM courses').fetchall()
    cursor.close()
    return rows

def insert_course(name: str, metrix_id: int, layout_ids: str, events: str) -> None:
    cursor = connection.cursor()
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    cursor.execute('INSERT INTO courses (name, metrix_id, layout_ids, events, updated_at) VALUES (?, ?, ?, ?, ?)', [name, metrix_id, layout_ids, events, timestamp])
    connection.commit()
    logger.info(f'Inserted new course to database with course_id: {metrix_id}')
    cursor.close()
    return

def update_course_events(events: str, metrix_id: int):
    cursor = connection.cursor()
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    cursor.execute('UPDATE courses SET events = ?, updated_at = ? WHERE metrix_id = ?', [events, timestamp, metrix_id])
    connection.commit()
    logger.info(f'Updated course: {metrix_id}')
    cursor.close()
    return
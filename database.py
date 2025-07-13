import sqlite3
from typing import List, Tuple

class Database:
    def __init__(self, db_name: str = "student_tracker.db"):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        with self.get_connection() as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    subject TEXT NOT NULL,
                    grade REAL NOT NULL,
                    date_recorded DATE DEFAULT CURRENT_DATE,
                    FOREIGN KEY (student_id) REFERENCES students (id)
                );
            ''')
    
    def add_student(self, name: str, email: str) -> bool:
        try:
            with self.get_connection() as conn:
                conn.execute("INSERT INTO students (name, email) VALUES (?, ?)", (name, email))
                return True
        except sqlite3.IntegrityError:
            return False
    
    def add_grade(self, student_id: int, subject: str, grade: float) -> bool:
        with self.get_connection() as conn:
            conn.execute("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)", 
                        (student_id, subject, grade))
            return True
    
    def get_students(self) -> List[Tuple]:
        with self.get_connection() as conn:
            return conn.execute("SELECT * FROM students").fetchall()
    
    def get_student_grades(self, student_id: int) -> List[Tuple]:
        with self.get_connection() as conn:
            return conn.execute('''
                SELECT s.name, g.subject, g.grade, g.date_recorded 
                FROM students s JOIN grades g ON s.id = g.student_id 
                WHERE s.id = ?
            ''', (student_id,)).fetchall()
    
    def get_student_average(self, student_id: int) -> float:
        with self.get_connection() as conn:
            result = conn.execute("SELECT AVG(grade) FROM grades WHERE student_id = ?", (student_id,)).fetchone()
            return result[0] if result[0] else 0.0
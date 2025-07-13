# Student Performance Tracker - Documentation

## Overview
A Python application for tracking student grades with both CLI and GUI interfaces using SQLite database.

## Installation
No installation required - uses Python built-in libraries only.

## Quick Start
```bash
# CLI Version
python tracker.py

# GUI Version  
python gui.py
```

## Features
- ✅ Add students with name and email
- ✅ Record grades for multiple subjects
- ✅ View all students
- ✅ Calculate average grades
- ✅ Performance reports

## File Structure
```
Student Performance Tracker/
├── database.py      # Database operations
├── tracker.py       # CLI interface
├── gui.py          # GUI interface
├── README.md       # Basic info
└── requirements.txt # Dependencies
```

## Database Schema
```sql
-- Students table
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- Grades table
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT NOT NULL,
    grade REAL NOT NULL,
    date_recorded DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (student_id) REFERENCES students (id)
);
```

## API Reference

### Database Class
```python
from database import Database

db = Database()
```

**Methods:**
- `add_student(name, email)` - Add new student
- `add_grade(student_id, subject, grade)` - Record grade
- `get_students()` - Get all students
- `get_student_grades(student_id)` - Get student's grades
- `get_student_average(student_id)` - Calculate average

### CLI Usage
```bash
python tracker.py
# Follow menu prompts:
# 1. Add Student
# 2. Record Grade  
# 3. View Students
# 4. View Performance
# 5. Exit
```

### GUI Usage
```bash
python gui.py
```
**Tabs:**
- **Add Student** - Form to register students
- **Record Grade** - Select student and add grades
- **View Performance** - Display grades and averages

## Examples

### Adding a Student
```python
from database import Database
db = Database()
db.add_student("John Doe", "john@email.com")
```

### Recording Grades
```python
db.add_grade(1, "Math", 85.5)
db.add_grade(1, "Science", 92.0)
```

### Viewing Performance
```python
grades = db.get_student_grades(1)
average = db.get_student_average(1)
```

## Validation Rules
- **Names**: Required, non-empty
- **Emails**: Required, unique
- **Grades**: 0-100 range
- **Subjects**: Required, non-empty

## Error Handling
- Duplicate email prevention
- Input validation
- Database connection errors
- Invalid grade ranges

## Performance Features
- Automatic average calculation
- Performance indicators:
  - 🏆 90-100: Excellent
  - ⭐ 80-89: Good  
  - 👍 70-79: Satisfactory
  - 📈 <70: Needs Improvement

## Troubleshooting

**Database Issues:**
- Database file created automatically
- Located in project directory as `student_tracker.db`

**GUI Issues:**
- Requires tkinter (included with Python)
- Refresh buttons update student lists

**Common Errors:**
- Email already exists → Use different email
- Invalid grade → Enter 0-100 range
- No student selected → Choose from dropdown

## Technical Details
- **Language**: Python 3.x
- **Database**: SQLite3
- **GUI**: tkinter
- **Dependencies**: None (built-in libraries only)
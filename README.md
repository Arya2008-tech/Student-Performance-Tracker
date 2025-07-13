# Student Performance Tracker

A minimal Python application to track student grades using SQLite database.

## Features
- Add students with name and email
- Record grades for different subjects
- View all students
- View individual student performance with average grade

## Usage

**Command Line Interface:**
```bash
python tracker.py
```

**Graphical User Interface:**
```bash
python gui.py
```

## Database Schema
- **students**: id, name, email
- **grades**: id, student_id, subject, grade, date_recorded
from database import Database

class StudentTracker:
    def __init__(self):
        self.db = Database()
    
    def add_student(self, name: str, email: str):
        if self.db.add_student(name, email):
            print(f"Student {name} added successfully!")
        else:
            print("Error: Email already exists!")
    
    def record_grade(self, student_id: int, subject: str, grade: float):
        if 0 <= grade <= 100:
            self.db.add_grade(student_id, subject, grade)
            print(f"Grade {grade} recorded for {subject}")
        else:
            print("Grade must be between 0 and 100")
    
    def view_students(self):
        students = self.db.get_students()
        if not students:
            print("No students found.")
            return
        
        print("\n--- Students ---")
        for student in students:
            print(f"ID: {student[0]}, Name: {student[1]}, Email: {student[2]}")
    
    def view_performance(self, student_id: int):
        grades = self.db.get_student_grades(student_id)
        if not grades:
            print("No grades found for this student.")
            return
        
        print(f"\n--- Performance for {grades[0][0]} ---")
        for grade in grades:
            print(f"{grade[1]}: {grade[2]} (Date: {grade[3]})")
        
        avg = self.db.get_student_average(student_id)
        print(f"Average Grade: {avg:.2f}")
    
    def run(self):
        while True:
            print("\n=== Student Performance Tracker ===")
            print("1. Add Student")
            print("2. Record Grade")
            print("3. View Students")
            print("4. View Student Performance")
            print("5. Exit")
            
            choice = input("Choose option: ").strip()
            
            if choice == "1":
                name = input("Student name: ").strip()
                email = input("Student email: ").strip()
                self.add_student(name, email)
            
            elif choice == "2":
                self.view_students()
                try:
                    student_id = int(input("Student ID: "))
                    subject = input("Subject: ").strip()
                    grade = float(input("Grade (0-100): "))
                    self.record_grade(student_id, subject, grade)
                except ValueError:
                    print("Invalid input!")
            
            elif choice == "3":
                self.view_students()
            
            elif choice == "4":
                self.view_students()
                try:
                    student_id = int(input("Student ID: "))
                    self.view_performance(student_id)
                except ValueError:
                    print("Invalid student ID!")
            
            elif choice == "5":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice!")

if __name__ == "__main__":
    tracker = StudentTracker()
    tracker.run()
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class StudentTrackerGUI:
    def __init__(self):
        self.db = Database()
        self.root = tk.Tk()
        self.root.title("Student Performance Tracker")
        self.root.geometry("600x500")
        self.setup_ui()
    
    def setup_ui(self):
        # Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add Student Tab
        add_frame = ttk.Frame(notebook)
        notebook.add(add_frame, text="Add Student")
        
        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.name_entry = ttk.Entry(add_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Email:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.email_entry = ttk.Entry(add_frame, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(add_frame, text="Add Student", command=self.add_student).grid(row=2, column=1, pady=10)
        
        # Record Grade Tab
        grade_frame = ttk.Frame(notebook)
        notebook.add(grade_frame, text="Record Grade")
        
        ttk.Label(grade_frame, text="Student:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.student_combo = ttk.Combobox(grade_frame, width=27, state="readonly")
        self.student_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(grade_frame, text="Subject:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.subject_entry = ttk.Entry(grade_frame, width=30)
        self.subject_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(grade_frame, text="Grade:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.grade_entry = ttk.Entry(grade_frame, width=30)
        self.grade_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(grade_frame, text="Record Grade", command=self.record_grade).grid(row=3, column=1, pady=10)
        ttk.Button(grade_frame, text="Refresh Students", command=self.refresh_students).grid(row=4, column=1, pady=5)
        
        # View Performance Tab
        view_frame = ttk.Frame(notebook)
        notebook.add(view_frame, text="View Performance")
        
        ttk.Label(view_frame, text="Select Student:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.view_combo = ttk.Combobox(view_frame, width=27, state="readonly")
        self.view_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(view_frame, text="View Grades", command=self.view_performance).grid(row=0, column=2, padx=5)
        ttk.Button(view_frame, text="Refresh", command=self.refresh_view_students).grid(row=1, column=1, pady=5)
        
        # Results display
        self.result_text = tk.Text(view_frame, height=20, width=70)
        self.result_text.grid(row=2, column=0, columnspan=3, padx=5, pady=10)
        
        scrollbar = ttk.Scrollbar(view_frame, orient="vertical", command=self.result_text.yview)
        scrollbar.grid(row=2, column=3, sticky='ns')
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.refresh_students()
        self.refresh_view_students()
    
    def add_student(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not name or not email:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        if self.db.add_student(name, email):
            messagebox.showinfo("Success", f"Student {name} added successfully!")
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.refresh_students()
            self.refresh_view_students()
        else:
            messagebox.showerror("Error", "Email already exists!")
    
    def record_grade(self):
        if not self.student_combo.get():
            messagebox.showerror("Error", "Please select a student")
            return
        
        try:
            student_id = int(self.student_combo.get().split(" - ")[0])
            subject = self.subject_entry.get().strip()
            grade = float(self.grade_entry.get())
            
            if not subject:
                messagebox.showerror("Error", "Please enter subject")
                return
            
            if not 0 <= grade <= 100:
                messagebox.showerror("Error", "Grade must be between 0 and 100")
                return
            
            self.db.add_grade(student_id, subject, grade)
            messagebox.showinfo("Success", f"Grade {grade} recorded for {subject}")
            self.subject_entry.delete(0, tk.END)
            self.grade_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid grade value")
    
    def view_performance(self):
        if not self.view_combo.get():
            messagebox.showerror("Error", "Please select a student")
            return
        
        student_id = int(self.view_combo.get().split(" - ")[0])
        grades = self.db.get_student_grades(student_id)
        
        self.result_text.delete(1.0, tk.END)
        
        if not grades:
            self.result_text.insert(tk.END, "No grades found for this student.")
            return
        
        student_name = grades[0][0]
        self.result_text.insert(tk.END, f"Performance for {student_name}\n")
        self.result_text.insert(tk.END, "=" * 40 + "\n\n")
        
        for grade in grades:
            self.result_text.insert(tk.END, f"Subject: {grade[1]}\n")
            self.result_text.insert(tk.END, f"Grade: {grade[2]}\n")
            self.result_text.insert(tk.END, f"Date: {grade[3]}\n")
            self.result_text.insert(tk.END, "-" * 20 + "\n")
        
        avg = self.db.get_student_average(student_id)
        self.result_text.insert(tk.END, f"\nAverage Grade: {avg:.2f}")
    
    def refresh_students(self):
        students = self.db.get_students()
        student_list = [f"{s[0]} - {s[1]}" for s in students]
        self.student_combo['values'] = student_list
    
    def refresh_view_students(self):
        students = self.db.get_students()
        student_list = [f"{s[0]} - {s[1]}" for s in students]
        self.view_combo['values'] = student_list
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StudentTrackerGUI()
    app.run()
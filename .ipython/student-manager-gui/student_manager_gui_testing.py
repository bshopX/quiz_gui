import csv
import tkinter as tk
from tkinter import ttk, messagebox



class StudentManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("500x400")

        self.students = {}

        # Title
        tk.Label(root, text="Student Manager", font=("Arial", 18, "bold")).pack(pady=10)

        # Input Frame
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Student Name").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(frame, text="Score").grid(row=1, column=0, padx=5)
        self.score_entry = tk.Entry(frame)
        self.score_entry.grid(row=1, column=1)

        tk.Button(root, text="Add Student", command=self.add_student).pack(pady=5)
        tk.Button(root, text="Save to CSV", command=self.save_to_csv).pack(pady=5)
        tk.Button(root, text="Load from CSV", command=self.load_from_csv).pack(pady=5)
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Search Student", command=self.search_student).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Delete Student", command=self.delete_student).grid(row=0, column=1, padx=5)
        
        # Table
        self.tree = ttk.Treeview(root, columns=("Name", "Score", "Grade"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Score", text="Score")
        self.tree.heading("Grade", text="Grade")
        self.tree.pack(fill="both", expand=True, pady=10)

    def calculate_grade(self, score):
        if score >= 70:
            return "A"
        elif score >= 60:
            return "B"
        elif score >= 50:
            return "C"
        elif score >= 45:
            return "D"
        else:
            return "F"

    def add_student(self):
        name = self.name_entry.get().strip()
        score = self.score_entry.get().strip()

        if not name or not score:
            messagebox.showerror("Error", "All fields are required")
            return

        if not score.isdigit():
            messagebox.showerror("Error", "Score must be a number")
            return

        score = int(score)
        grade = self.calculate_grade(score)

        self.tree.insert("", "end", values=( name, score, grade))

        self.name_entry.delete(0, tk.END)
        self.score_entry.delete(0, tk.END)
        
    def search_student(self):
        name = self.name_entry.get().strip()
        found = False
        
        for item in self.tree.get_children():
            values = self.tree.item(item) ["values"]
            if name and name in self.tree.item(item)["values"]:
                found = True
                
            if not found:
                messagebox.showinfo("Search", "Student not found")
                
            else:
                messagebox.showinfo("Search", "Student exists in the list")
                
    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Delete", "Select a student to delete")
            return
        
        self.tree.delete(selected)
        
    def save_to_csv(self):
        with open("student.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Score", "Grade"])
            
            for item in self.tree.get_children():
                name, score, grade = self.tree.item(item)["values"]
                
                writer.writerow([name, score, grade])
                messagebox.showinfo("Saved", "Students saved to students.csv")
    
    def load_from_csv(self):
        try:
            with open("students.csv", "r") as file:
                reader = csv.reader(file)
            next(reader)

            for row in self.tree.get_children():
                self.tree.delete(row)

            for name, score, grade in reader:
                self.tree.insert("", "end", values=(name, int(score), grade))

            messagebox.showinfo("Loaded", "Students loaded from CSV")

        except FileNotFoundError:
          messagebox.showerror("Error", "students.csv not found")


if __name__ == "__main__":
    root = tk.Tk()
    StudentManagerGUI(root)
    root.mainloop()

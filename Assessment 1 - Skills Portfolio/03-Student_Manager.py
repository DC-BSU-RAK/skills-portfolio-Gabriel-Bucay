import tkinter as tk
from tkinter import messagebox, simpledialog
import os

# Load student data from file
def load_students(filename="A1 - Resources/studentMarks.txt"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)
    
    students = []
    with open(file_path, "r") as f:
        n = int(f.readline().strip())
        for line in f:
            parts = line.strip().split(",")
            code = int(parts[0])
            name = parts[1]
            coursework = sum(map(int, parts[2:5]))
            exam = int(parts[5])
            total = coursework + exam
            percentage = (total / 160) * 100
            grade = get_grade(percentage)
            students.append({
                "code": code,
                "name": name,
                "coursework": coursework,
                "exam": exam,
                "percentage": percentage,
                "grade": grade
            })
    return students

# -------------------------------
# Grade calculation
# -------------------------------
def get_grade(percentage):
    if percentage >= 70: return "A"
    elif percentage >= 60: return "B"
    elif percentage >= 50: return "C"
    elif percentage >= 40: return "D"
    else: return "F"

# -------------------------------
# GUI Functions
# -------------------------------
def display_student(s):
    output_text = (
        f"👤 {s['name']} ({s['code']})\n"
        f"📘 Coursework: {s['coursework']} / 60\n"
        f"📝 Exam: {s['exam']} / 100\n"
        f"📊 Overall: {s['percentage']:.2f}%\n"
        f"🏅 Grade: {s['grade']}\n\n"
    )
    return output_text

def view_all_students():
    output.delete("1.0", tk.END)
    total_percent = 0
    for s in students:
        output.insert(tk.END, display_student(s))
        total_percent += s['percentage']
    avg = total_percent / len(students)
    output.insert(tk.END, f"📌 Summary\n")
    output.insert(tk.END, f"👥 Students: {len(students)}\n")
    output.insert(tk.END, f"📈 Average: {avg:.2f}%\n")

def view_student():
    code = simpledialog.askinteger("Student Lookup", "Enter student code:")
    output.delete("1.0", tk.END)
    for s in students:
        if s["code"] == code:
            output.insert(tk.END, display_student(s))
            return
    messagebox.showerror("Error", "Student not found!")

def highest_score():
    top = max(students, key=lambda s: s["percentage"])
    output.delete("1.0", tk.END)
    output.insert(tk.END, "🏆 Highest Scorer\n")
    output.insert(tk.END, display_student(top))

def lowest_score():
    low = min(students, key=lambda s: s["percentage"])
    output.delete("1.0", tk.END)
    output.insert(tk.END, "🔻 Lowest Scorer\n")
    output.insert(tk.END, display_student(low))

# -------------------------------
# Main GUI Setup
# -------------------------------
root = tk.Tk()
root.title("Student Manager")
root.geometry("600x500")
root.configure(bg="#1e1e1e")

# Custom font and colors
FONT = ("Segoe UI", 11)
TEXT_BG = "#2b2b2b"
TEXT_FG = "#f0f0f0"
BTN_BG = "#3c3f41"
BTN_FG = "#ffffff"
ACCENT = "#00bcd4"

# Menu bar
menu = tk.Menu(root, bg=BTN_BG, fg=BTN_FG, activebackground=ACCENT, activeforeground="white")
root.config(menu=menu)

menu.add_command(label="📋 View All", command=view_all_students)
menu.add_command(label="🔍 View One", command=view_student)
menu.add_command(label="🏆 Highest", command=highest_score)
menu.add_command(label="🔻 Lowest", command=lowest_score)

# Output frame
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
                 bg=TEXT_BG, fg=TEXT_FG, font=FONT, insertbackground="white")
output.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=output.yview)

# Load data
students = load_students()

# Start GUI
root.mainloop()
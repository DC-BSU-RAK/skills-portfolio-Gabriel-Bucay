import tkinter as tk
from tkinter import messagebox
import random

#Difficulty select
DIFFICULTY_RANGES = {
    'Easy': (1, 9),
    'Moderate': (10, 99),
    'Advanced': (1000, 9999)
}

class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
        self.root.geometry("800x600")
        self.root.configure(bg="#03112c")  # background

        self.score = 0
        self.question_count = 0
        self.attempt = 1
        self.difficulty = None
        self.current_question = None
        self.answer = None

        # Score 
        self.score_var = tk.StringVar()
        self.score_var.set("Score: 0")
        self.score_label = tk.Label(self.root, textvariable=self.score_var,
                                    font=("Helvetica", 14, "bold"), fg="#004080", bg="#f0f4fc")
        self.score_label.place(relx=0.95, rely=0.05, anchor="ne")

        self.displayMenu()
    #Display
    def displayMenu(self):
        self.clearWindow()
        frame = tk.Frame(self.root, bg="#99b8f6")
        frame.pack(expand=True)

        tk.Label(frame, text="Select Difficulty Level", font=("Helvetica", 24, "bold"),
                 bg="#99b8f6", fg="#00264d").pack(pady=30)
        #Buttons for difficulty
        for level in DIFFICULTY_RANGES.keys():
            tk.Button(frame, text=level, width=20, font=("Helvetica", 16),
                      bg="#cce6ff", fg="#00264d", activebackground="#99ccff",
                      command=lambda l=level: self.startQuiz(l)).pack(pady=10)
    #Gets random variable per ifficulty
    def randomInt(self):
        min_val, max_val = DIFFICULTY_RANGES[self.difficulty]
        return random.randint(min_val, max_val)

    def decideOperation(self):
        return random.choice(['+', '-'])

    def displayProblem(self):
        self.clearWindow()
        self.updateScoreLabel()
        #Shows Operations
        num1 = self.randomInt()
        num2 = self.randomInt()
        op = self.decideOperation()
        self.current_question = f"{num1} {op} {num2}"
        self.answer = eval(self.current_question)

        frame = tk.Frame(self.root, bg="#f0f4fc")
        frame.pack(expand=True)

        tk.Label(frame, text=f"Question {self.question_count + 1} of 10",
                 font=("Helvetica", 18), bg="#f0f4fc", fg="#003366").pack(pady=10)

        tk.Label(frame, text=self.current_question + " =",
                 font=("Helvetica", 28, "bold"), bg="#f0f4fc", fg="#000000").pack(pady=20)
        #User Answers
        self.answer_entry = tk.Entry(frame, font=("Helvetica", 20), justify="center", width=10)
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus()
        #Enter Button
        tk.Button(frame, text="Submit", font=("Helvetica", 16),
                  bg="#cce6ff", fg="#00264d", activebackground="#99ccff",
                  command=self.checkAnswer).pack(pady=20)

    def isCorrect(self, user_input):
        try:
            return int(user_input) == self.answer
        except ValueError:
            return False

    def displayResults(self):
        self.clearWindow()
        grade = self.getGrade(self.score)

        frame = tk.Frame(self.root, bg="#f0f4fc")
        frame.pack(expand=True)

        tk.Label(frame, text=f"Final Score: {self.score}/100",
                 font=("Helvetica", 22, "bold"), bg="#f0f4fc", fg="#004080").pack(pady=20)
        tk.Label(frame, text=f"Grade: {grade}",
                 font=("Helvetica", 20), bg="#f0f4fc", fg="#003366").pack(pady=10)
        #Replay/Exit button
        tk.Button(frame, text="Play Again", font=("Helvetica", 16),
                  bg="#cce6ff", fg="#00264d", activebackground="#99ccff",
                  command=self.displayMenu).pack(pady=10)
        tk.Button(frame, text="Exit", font=("Helvetica", 16),
                  bg="#ffcccc", fg="#660000", activebackground="#ff9999",
                  command=self.root.quit).pack(pady=5)
    #Grade at the end of the quiz
    def getGrade(self, score):
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        else:
            return "F"
    #Answe checker
    def checkAnswer(self):
        user_input = self.answer_entry.get()
        if self.isCorrect(user_input):
            points = 10 if self.attempt == 1 else 5
            self.score += points
            self.updateScoreLabel()
            messagebox.showinfo("Correct!", f"Correct! You earned {points} points.")
            self.question_count += 1
            self.attempt = 1
        else:
            if self.attempt == 1:
                messagebox.showwarning("Try Again", "Incorrect. Try once more.")
                self.attempt += 1
                return
            else:
                messagebox.showerror("Wrong", f"Wrong again. The correct answer was {self.answer}.")
                self.question_count += 1
                self.attempt = 1
        #Continue or shut down
        if self.question_count < 10:
            self.displayProblem()
        else:
            self.displayResults()
    #Score label
    def updateScoreLabel(self):
        self.score_var.set(f"Score: {self.score}")
        self.score_label.place(relx=0.95, rely=0.05, anchor="ne")

    def clearWindow(self):
        for widget in self.root.winfo_children():
            if widget != self.score_label:
                widget.destroy()
    #Start after difficulty set
    def startQuiz(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        self.question_count = 0
        self.attempt = 1
        self.updateScoreLabel()
        self.displayProblem()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop() 
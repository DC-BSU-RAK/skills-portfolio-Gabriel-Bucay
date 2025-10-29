import tkinter as tk
from tkinter import messagebox
import random
import os

class JokeAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joker Assistant")
        self.root.geometry("400x300") #window size

        # Load jokes from file 
        base_dir = os.path.dirname(__file__)
        jokes_path = os.path.join(base_dir, "A1 - Resources", "randomJokes.txt")
        self.jokes = self.load_jokes(jokes_path)
        self.current_joke = None

        # Set up the GUI layout
        self.setup_gui()

    #helps read and format the jokes from the randomJokes.txt 
    def load_jokes(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
                jokes = []
                for line in lines:
                    if "?" in line:
                        setup, punchline = line.strip().split("?", 1)
                        jokes.append((setup + "?", punchline.strip()))
                return jokes
        except FileNotFoundError:
            messagebox.showerror("File Error", f"Could not find {filename}.")
            return []
        
        print(f"Trying to load jokes from: {filename}")

    #GUI setup and word designs
    def setup_gui(self):
        """
        Create and place all GUI widgets: labels and buttons.
        """
        # Label to show the joke setup
        self.setup_label = tk.Label(self.root, text="", font=("Courier New", 14), wraplength=400, justify="left")
        self.setup_label.pack(pady=10)

        # Label to show the punchline (initially empty)
        self.punchline_label = tk.Label(self.root, text="", font=("Courier New", 12), fg="gray", wraplength=400, justify="left")
        self.punchline_label.pack(pady=5)

        #Frame for the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        #Style
        button_style = {
            "font": ("Georgia", 11, "bold"),
            "bg": "#8E4CAF",       # Green background
            "fg": "white",         # White text
            "activebackground": "#2d165f",  # Slightly darker on hover
            "width": 20,
            "bd": 2,
            "relief": "ridge"
        }
        # Buttons 
        tk.Button(self.root, text="Alexa tell me a Joke", command=self.tell_joke, **button_style).pack(pady=5)
        tk.Button(self.root, text="Show Punchline", command=self.show_punchline, **button_style).pack(pady=5)
        tk.Button(self.root, text="Next Joke", command=self.tell_joke, **button_style).pack(pady=5)
        tk.Button(self.root, text="Quit", command=self.root.quit, **button_style).pack(pady=10)

    def tell_joke(self):

        if not self.jokes:
            self.setup_label.config(text="No jokes available.")
            self.punchline_label.config(text="")
            return

        # Random joke picker
        self.current_joke = random.choice(self.jokes)
        self.setup_label.config(text=self.current_joke[0])
        self.punchline_label.config(text="")  #only shows puncline if clicked

    def show_punchline(self):
        
        if self.current_joke:
            self.punchline_label.config(text=self.current_joke[1])
        else:
            messagebox.showinfo("No Joke", "Click 'Alexa tell me a Joke' first!")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = JokeAssistantApp(root)
    root.mainloop()
import tkinter as tk
import random

#stores Questions and Answers in dictionary.
QUIZ_DATA = [
    {"q": "Which data structure follows FIFO?",
     "options": {"A": "Stack", "B": "Queue", "C": "Tree", "D": "Graph"}, "answer": "B"},

    {"q": "Time complexity of binary search?",
     "options": {"A": "O(1)", "B": "O(n)", "C": "O(log n)", "D": "O(n^2)"}, "answer": "C"},

    {"q": "Which is NOT a linear data structure?",
     "options": {"A": "Array", "B": "Linked List", "C": "Queue", "D": "Tree"}, "answer": "D"},

    {"q": "What does LIFO stand for?",
     "options": {"A": "Last In First Out", "B": "List In First Out", "C": "Last In Forward Out", "D": "Line In First Out"}, "answer": "A"},

    {"q": "Which data structure uses LIFO order?",
     "options": {"A": "Queue", "B": "Stack", "C": "Array", "D": "Linked List"}, "answer": "B"},

    {"q": "What is the worst-case time complexity of quicksort?",
     "options": {"A": "O(n log n)", "B": "O(n)", "C": "O(n^2)", "D": "O(log n)"}, "answer": "C"},

    {"q": "Which data structure is used to implement recursion internally?",
     "options": {"A": "Queue", "B": "Stack", "C": "Heap", "D": "Graph"}, "answer": "B"},

    {"q": "In a binary tree, a node with no children is called a:",
     "options": {"A": "Root", "B": "Leaf", "C": "Parent", "D": "Sibling"}, "answer": "B"},

    {"q": "Which data structure allows insertion and deletion from both ends?",
     "options": {"A": "Stack", "B": "Queue", "C": "Deque", "D": "Array"}, "answer": "C"},

    {"q": "What is the time complexity of accessing an element in an array by index?",
     "options": {"A": "O(1)", "B": "O(n)", "C": "O(log n)", "D": "O(n^2)"}, "answer": "A"},
]

#makes it easier to change color in the entire code.
BACKGROUND_COLOR = "#1e1e2e"
TEXT_COLOR = "#e0e0f0"
HIGHLIGHT_COLOR = "#7aa2f7"
CORRECT_COLOR = "#8fd19e"
WRONG_COLOR = "#ff1500"
WARNING_COLOR = "#ffc64c"


class QuizApp:
    TIME_LIMIT = 30
    DELAY = 1000
    
    #creates the main window and frame.
    def __init__(self, root, data):
        self.root = root
        root.title("Quiz App")
        root.geometry("750x550")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        #defining conts.
        self.questions = random.sample(data, len(QUIZ_DATA))
        self.score = 0
        self.index = 0
        self.time_left = self.TIME_LIMIT
        self.timer_id = None
        self.choice = tk.StringVar()
        #creates a frame
        self.main_frame = tk.Frame(root, bg=BACKGROUND_COLOR,
                            highlightthickness=1, highlightbackground="black")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        #creates labels like heading, timer, questions and answers.
        self.heading_label = self.make_label(size=30, bold=True, color="light grey")
        self.heading_label.configure(text="QUIZ")
        self.timer_label = self.make_label(size=15, bold=True, color=WARNING_COLOR)
        self.question_label = self.make_label(size=18, wrap_width=750)
        self.feedback_label = self.make_label(size=14, bold=True)
        self.submit_button = tk.Button(self.main_frame, text="Submit Answer",
                                        font=("Segoe UI", 14), command=self.check_answer,
                                        bg=HIGHLIGHT_COLOR, fg=BACKGROUND_COLOR,
                                        relief="ridge", padx=10, pady=5, cursor="hand2")

        self.option_buttons = [tk.Radiobutton(self.main_frame, variable=self.choice,
                                               font=("Segoe UI", 16), bg=BACKGROUND_COLOR,
                                               fg=TEXT_COLOR, selectcolor="#1d1d3c",
                                               highlightthickness=0)
                                for _ in range(4)]

        # grid places the widgets in the organised place according to the row and column.
        self.heading_label.grid(row=0, column=0, sticky="new")
        self.timer_label.grid(row=0, column=1, padx=5, pady= 5, sticky="new")
        self.question_label.grid(row=1, column=0, padx=5, pady= 20, sticky="n")
        for row_number, option_button in enumerate(self.option_buttons, start=2):
            option_button.grid(row=row_number, column=0, sticky="w", padx=50, pady=5)
        self.submit_button.grid(row=6, column=0, padx=5, pady= 5)
        self.feedback_label.grid(row=7, column=0, padx=5, pady= 5, sticky="nsew")

        self.load_question()

    #sets the arguments and parameters for all the labels in the entire code
    def make_label(self, size, bold=False, color=TEXT_COLOR, wrap_width=0):
        weight = "bold" if bold else "normal"
        return tk.Label(self.main_frame, font=("Segoe UI", size, weight),
                         fg=color, bg=BACKGROUND_COLOR, wraplength=wrap_width)

    #displays questions and options in the frame
    def load_question(self):
        if self.index >= len(self.questions):
            self.end_quiz()
            return

        self.time_left = self.TIME_LIMIT
        self.choice.set(None)
        self.feedback_label.config(text="")
        self.submit_button.config(state="normal")

        current_question = self.questions[self.index]
        self.question_label.config(text=f"Q{self.index + 1}: {current_question['q']}")
        for option_button, (key, value) in zip(self.option_buttons, current_question["options"].items()):
            option_button.config(text=f"{key}. {value}", value=key)

        self.tick()

    #runs the timer
    def tick(self):
        self.timer_label.config(text=f"Time: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.tick)
        else:
            self.finish_question(timeout=True)

    #runs when submit button is clicked without selecting any option
    def check_answer(self):
        if self.choice.get() in ("", "None"):
            self.feedback_label.config(text="Please select an answer!", fg=WARNING_COLOR)
            return
        self.finish_question(timeout=False)

    #verifies the answer and gives feedback
    def finish_question(self, timeout):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.submit_button.config(state="disabled")

        c = self.questions[self.index]["answer"]
        if timeout:
            self.feedback_label.config(text="Time's Up!", fg=WARNING_COLOR)
        elif self.choice.get() == c:
            self.score += 1
            self.feedback_label.config(text="Correct!", fg=CORRECT_COLOR)
        else:
            self.feedback_label.config(text=f"Wrong! Correct answer: {c}", fg=WRONG_COLOR)
        #time between the current question and next question after submitting
        self.root.after(self.DELAY, self.advance)

    #loads next question after current question is submitted
    def advance(self):
        self.index += 1
        self.load_question()

    #creates the score cars screen
    def end_quiz(self):
        #destroys current widgets in the frame and calculates the percentage.
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        percent_score = self.score / len(self.questions) * 100

        #creates new widgets in the frame for the score card.
        title_label = self.make_label(16, bold=True, color=HIGHLIGHT_COLOR)
        title_label.config(text="=== Quiz Complete ===")
        title_label.grid(row=0, column=0, pady=40)

        score_label = self.make_label(14)
        score_label.config(text=f"Final Score: {self.score} / {len(self.questions)}")
        score_label.grid(row=1, column=0, pady=10)

        percent_label = self.make_label(14)
        percent_label.config(text=f"Percentage: {percent_score:.1f}%")
        percent_label.grid(row=2, column=0, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    QuizApp(root, QUIZ_DATA)
    root.mainloop()
# GUI Quiz (Full Example) - Level 1 DTC
# --------------------------------------------------------------
# A fully working Tkinter quiz with step-by-step comments.
# You can edit the questions to make it your own.
# --------------------------------------------------------------
 
import tkinter as tk
from tkinter import ttk, messagebox
 
# ------- Data for the quiz (edit these to make it yours) -------
questions = [
    {
        "text": "Which animal is a mammal?",
        "options": ["Tuatara", "Kea", "Dolphin", "Pāua"],
        "answer": "Dolphin",
    },
    {
        "text": "What does 'CPU' stand for?",
        "options": ["Central Processing Unit", "Computer Personal Unit", "Central Power Unit", "Control Program Utility"],
        "answer": "Central Processing Unit",
    },
    {
        "text": "Which symbol means 'equal to' in Python?",
        "options": ["=", "==", "!=", ">="],
        "answer": "==",
    },
    {
        "text": "In Python, which is a list? ",
        "options": ["{1, 2, 3}", "(1, 2, 3)", "[1, 2, 3]", "<1, 2, 3>"],
        "answer": "[1, 2, 3]",
    },
    {
        "text": "What is the output of print(3 * 2)?",
        "options": ["5", "6", "32", "3*2"],
        "answer": "6",
    },
]
 
# ------- App state (variables that remember things) -------
current_index = 0           # which question we are on (starts at 0 for the first)
score = 0                   # how many we have correct so far
selected_answer = None      # will become a tk.StringVar after we create the window
 
# ------- Create the main window -------
root = tk.Tk()
root.title("My Quiz")
root.geometry("520x420")  # width x height
 
# A main frame (box) with padding to keep things neat
main = ttk.Frame(root, padding=16)
main.pack(fill="both", expand=True)
 
# ------- Progress label (top right) -------
progress_label = ttk.Label(main, text="")  # we'll set the real text later
progress_label.pack(anchor="e")  # anchor=e means stick to the right
 
# ------- Question text -------
question_label = ttk.Label(main, text="", wraplength=480, justify="left", font=("Segoe UI", 12, "bold"))
question_label.pack(anchor="w", pady=(8, 6))
 
# ------- Where the options (radio buttons) go -------
options_frame = ttk.Frame(main)
options_frame.pack(fill="x", pady=(0, 8))
 
option_buttons = []  # we'll store the radio buttons here so we can remove them later
 
# This variable stores which option the user has chosen
selected_answer = tk.StringVar(value="")
 
# ------- Feedback area (shows Correct!/Try again) -------
feedback_label = ttk.Label(main, text="", foreground="#333")  # simple feedback text
feedback_label.pack(anchor="w", pady=(4, 8))
 
# ------- Buttons row -------
buttons = ttk.Frame(main)
buttons.pack(fill="x", pady=(8, 0))
 
submit_btn = ttk.Button(buttons, text="Submit")
submit_btn.pack(side="left")
 
next_btn = ttk.Button(buttons, text="Next", state="disabled")
next_btn.pack(side="left", padx=(8, 0))
 
quit_btn = ttk.Button(buttons, text="Quit", command=root.destroy)
quit_btn.pack(side="right")
 
 
def update_progress():
    """Show which question we are on and the current score."""
    progress_label.config(text=f"Question {current_index + 1} of {len(questions)}  |  Score: {score}")
 
 
def clear_options():
    """Remove any existing radio buttons before we add new ones."""
    for rb in option_buttons:
        rb.destroy()
    option_buttons.clear()
 
 
def load_question():
    """Display the current question and its options on the screen."""
    update_progress()
    feedback_label.config(text="")          # clear any previous feedback
    submit_btn.config(state="normal")       # allow the user to submit
    next_btn.config(state="disabled")       # disable next until they submit
    selected_answer.set("")                 # clear previous selection
 
    q = questions[current_index]             # get the current question (a dictionary)
 
    # Show the question text
    question_label.config(text=f"Q{current_index + 1}: {q['text']}")
 
    # Remove old radio buttons and create new ones
    clear_options()
    for option_text in q["options"]:
        rb = ttk.Radiobutton(
            options_frame,
            text=option_text,                 # what the user sees
            value=option_text,                # what goes into selected_answer if clicked
            variable=selected_answer,
        )
        rb.pack(anchor="w", pady=2)
        option_buttons.append(rb)
 
 
def submit_answer():
    """Check the selected answer and update the score and feedback."""
    global score
    choice = selected_answer.get()
 
    if choice == "":
        # They clicked submit without choosing anything
        messagebox.showinfo("Select an answer", "Please select one answer before submitting.")
        return
 
    correct = questions[current_index]["answer"]
 
    if choice == correct:
        score += 1
        feedback_label.config(text="✅ Correct!", foreground="green")
    else:
        feedback_label.config(text=f"❌ Not quite. Correct answer: {correct}", foreground="red")
 
    # After submitting, prevent multiple submissions for the same question
    submit_btn.config(state="disabled")
    next_btn.config(state="normal")
 
 
def next_question():
    """Go to the next question, or finish the quiz if we are at the end."""
    global current_index
    current_index += 1
 
    if current_index < len(questions):
        load_question()
    else:
        finish_quiz()
 
 
def finish_quiz():
    """Show the final score and offer to play again."""
    percent = int((score / len(questions)) * 100)
    again = messagebox.askyesno("Quiz complete", f"You scored {score} out of {len(questions)} ({percent}%).\n\nPlay again?")
    if again:
        restart_quiz()
    else:
        root.destroy()
 
 
def restart_quiz():
    """Reset everything and start from the first question again."""
    global current_index, score
    current_index = 0
    score = 0
    load_question()
 
 
# Connect the buttons to the functions above
submit_btn.config(command=submit_answer)
next_btn.config(command=next_question)
 
# Start the quiz by loading the first question
load_question()
 
# Start the app (this must be last)
root.mainloop()
 
 
import tkinter as tk
from tkinter import messagebox
from RecommendationEngine import RecommendationEngine
from MyFacts import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quality Control Recommendation System")
        self.geometry("800x600")
        self.configure(bg="#2E2E2E")

        self.engine = RecommendationEngine()
        self.questions = [
            {"id": "total", "text": "What is the batch size?", "type": "int"},
            {"id": "deffected", "text": "how many biscuits are deffected?", "type": "int"},
            {"id": "cracked", "text": "how many biscuits are cracked?", "type": "int"},
            {"id": "burned", "text": "how many biscuits are burned?", "type": "int"},
            {"id": "under_cooked", "text": "how many biscuits are under_cooked?", "type": "int"},
            {"id": "over_sized", "text": "how many biscuits are over_sized?", "type": "int"},
            {"id": "under_sized", "text": "how many biscuits are under_sized?", "type": "int"},
            {"id": "contaminated", "text": "how many biscuits are contaminated?", "type": "int"},
            {"id": "severly_cracked_count", "text": "How many severly cracked biscuits (>50%)?", "type": "int"},
            {"id": "moderate_cracked_count", "text": "How many moderate cracked biscuits (20%~50%)?", "type": "int"},
            {"id": "low_cracked_count", "text": "How many low cracked biscuits (<20%)?", "type": "int"},
            {"id": "severly_burned_count", "text": "How many severly burned biscuits (>40%)?", "type": "int"},
            {"id": "moderate_burned_count", "text": "How many moderate burned biscuits(10%~40%)?", "type": "int"},
            {"id": "low_burned_count", "text": "How many low burned biscuits(<10%)?", "type": "int"},
            {"id": "severly_under_cooked_count", "text": "How many severly under_cooked biscuits (>40%)?", "type": "int"},
            {"id": "moderate_under_cooked_count", "text": "How many moderate under_cooked biscuits(10%~40%)?", "type": "int"},
            {"id": "low_under_cooked_count", "text": "How many low under_cooked biscuits(<10%)?", "type": "int"},
            {"id": "severely_over_sized_count", "text": "How many biscuits have raduis greater than 4cm", "type": "int"},
            {"id": "moderate_over_sized_count", "text": "How many biscuits have raduis between 3.5cm and 4cm?", "type": "int"},
            {"id": "moderate_under_sized_count", "text": "How many biscuits have raduis between 2.5cm and 3cm?", "type": "int"},
            {"id": "severly_under_sized_count", "text": "How many biscuits have raduis lower than 2.5cm?", "type": "int"},
        ]
        self.current_question_index = 0
        self.answers = {}

        self.question_label = tk.Label(self, text="", wraplength=780, font=("Segoe UI", 14), bg="#2E2E2E", fg="#FFFFFF")
        self.question_label.pack(pady=20)

        self.entry = tk.Entry(self, font=("Segoe UI", 12), bg="#3C3C3C", fg="#FFFFFF", insertbackground="#FFFFFF", borderwidth=0)
        self.entry.pack(pady=10)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_answer, font=("Segoe UI", 12, "bold"), bg="#4A90E2", fg="#FFFFFF", borderwidth=0, relief="flat", activebackground="#357ABD", activeforeground="#FFFFFF")
        self.submit_button.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.ask_next_question()

    def ask_next_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.question_label.config(text=question["text"])
        else:
            self.run_engine_and_show_recommendations()

    def submit_answer(self):
        answer = self.entry.get()
        question = self.questions[self.current_question_index]

        if self.validate_answer(answer, question["type"]):
            self.answers[question["id"]] = answer
            self.current_question_index += 1
            self.entry.delete(0, tk.END)
            self.ask_next_question()
        else:
            messagebox.showerror("Invalid Input", "Please provide a valid input.")

    def validate_answer(self, answer, answer_type):
        if answer_type == "int":
            return answer.isdigit()
        return True

    def run_engine_and_show_recommendations(self):
        self.engine.reset()
        for fact_id, fact_value in self.answers.items():
            self.engine.declare(Answer(id=fact_id, text=fact_value))
        self.engine.run()
        recommendations = "\n".join(self.engine.recommendations)
        if not recommendations:
            recommendations = "No recommendations."

        recommendation_window = tk.Toplevel(self)
        recommendation_window.title("Recommendations")
        recommendation_window.configure(bg="#2E2E2E")

        recommendation_text = tk.Text(recommendation_window, wrap="word", height=20, width=80, font=("Segoe UI", 12), bg="#3C3C3C", fg="#FFFFFF", borderwidth=0)
        recommendation_text.pack(padx=10, pady=10)
        recommendation_text.insert(tk.END, recommendations)
        recommendation_text.config(state="disabled")

        self.question_label.config(text="Analysis complete. See recommendations.")
        self.entry.pack_forget()
        self.submit_button.pack_forget()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()

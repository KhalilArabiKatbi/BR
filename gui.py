import collections
import collections.abc
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping
import tkinter as tk
from tkinter import ttk
from RecommendationEngine import RecommendationEngine
from MyFacts import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Biscuit Quality Control")
        self.geometry("800x600")

        self.engine = RecommendationEngine()

        self.create_widgets()

    def create_widgets(self):
        # Create a canvas and a vertical scrollbar for scrolling the frame
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.inputs = {}
        questions = self.get_questions()

        for question_id, question_text in questions.items():
            label = ttk.Label(self.scrollable_frame, text=question_text)
            label.pack(anchor="w", padx=10, pady=5)
            entry = ttk.Entry(self.scrollable_frame, width=100)
            entry.pack(anchor="w", padx=10, pady=2, fill="x")
            self.inputs[question_id] = entry

        self.run_button = ttk.Button(self, text="Run Analysis", command=self.run_analysis)
        self.run_button.pack(pady=10)

        self.recommendation_text = tk.Text(self, wrap="word")
        self.recommendation_text.pack(fill="both", expand=True)

    def get_questions(self):
        questions = {}
        for fact in self.engine.facts.values():
            if isinstance(fact, Question):
                questions[fact['id']] = fact['text']
        return questions

    def run_analysis(self):
        self.engine.reset()

        for question_id, entry in self.inputs.items():
            answer = entry.get()
            question = self.get_question_by_id(question_id)
            if answer and question:
                validated_answer = self.engine.is_of_type(answer, question['Type'], question['valid'])
                if validated_answer is not None:
                    self.engine.declare(Answer(id=question_id, text=validated_answer))

        self.engine.run()

        self.recommendation_text.delete("1.0", "end")
        for fact in self.engine.facts.values():
            if "recommendation" in fact:
                self.recommendation_text.insert("end", fact["recommendation"] + "\n")
            elif isinstance(fact, Prediction):
                self.recommendation_text.insert("end", f"Prediction: {fact['text']} (CF: {fact['cf']})\n")

    def get_question_by_id(self, question_id):
        for fact in self.engine.facts.values():
            if isinstance(fact, Question) and fact['id'] == question_id:
                return fact
        return None

if __name__ == "__main__":
    app = App()
    app.mainloop()

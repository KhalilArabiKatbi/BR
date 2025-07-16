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
        self.question_label = ttk.Label(self, text="")
        self.question_label.pack(pady=10)

        self.answer_entry = ttk.Entry(self)
        self.answer_entry.pack(pady=10)

        self.submit_button = ttk.Button(self, text="Submit", command=self.submit_answer)
        self.submit_button.pack(pady=10)

        self.recommendation_text = tk.Text(self, wrap="word")
        self.recommendation_text.pack(fill="both", expand=True)

        self.engine.reset()
        self.ask_next_question()

    def ask_next_question(self):
        self.engine.run()
        for fact_index in self.engine.facts:
            fact = self.engine.facts[fact_index]
            if isinstance(fact, Fact) and fact.as_dict().get('__type__') == 'ask':
                question_id = fact.as_dict()['value']
                for q_fact_index in self.engine.facts:
                    q_fact = self.engine.facts[q_fact_index]
                    if isinstance(q_fact, Question) and q_fact['id'] == question_id:
                        self.question_label.config(text=q_fact['text'])
                        return
        self.display_recommendations()

    def submit_answer(self):
        answer = self.answer_entry.get()
        for fact_index in self.engine.facts:
            fact = self.engine.facts[fact_index]
            if isinstance(fact, Fact) and fact.as_dict().get('__type__') == 'ask':
                question_id = fact.as_dict()['value']
                for q_fact_index in self.engine.facts:
                    q_fact = self.engine.facts[q_fact_index]
                    if isinstance(q_fact, Question) and q_fact['id'] == question_id:
                        validated_answer = self.engine.is_of_type(answer, q_fact['Type'], q_fact['valid'])
                        if validated_answer is not None:
                            self.engine.declare(Answer(id=question_id, text=validated_answer))
                            self.answer_entry.delete(0, 'end')
                            self.ask_next_question()
                        else:
                            self.question_label.config(text="Invalid input. Please try again.\n" + q_fact['text'])
                        return

    def display_recommendations(self):
        self.question_label.config(text="Analysis Complete")
        self.answer_entry.pack_forget()
        self.submit_button.pack_forget()

        self.recommendation_text.delete("1.0", "end")
        for fact in self.engine.facts.values():
            if "recommendation" in fact:
                self.recommendation_text.insert("end", fact["recommendation"] + "\n")
            elif isinstance(fact, Prediction):
                self.recommendation_text.insert("end", f"Prediction: {fact['text']} (CF: {fact['cf']})\n")

if __name__ == "__main__":
    app = App()
    app.mainloop()

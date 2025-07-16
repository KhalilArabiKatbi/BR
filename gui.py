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
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Create tabs
        self.general_tab = ttk.Frame(self.notebook)
        self.cracked_tab = ttk.Frame(self.notebook)
        self.burned_tab = ttk.Frame(self.notebook)
        self.undercooked_tab = ttk.Frame(self.notebook)
        self.sized_tab = ttk.Frame(self.notebook)
        self.contaminated_tab = ttk.Frame(self.notebook)
        self.recommendations_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.general_tab, text="General")
        self.notebook.add(self.cracked_tab, text="Cracked")
        self.notebook.add(self.burned_tab, text="Burned")
        self.notebook.add(self.undercooked_tab, text="Under Cooked")
        self.notebook.add(self.sized_tab, text="Sized")
        self.notebook.add(self.contaminated_tab, text="Contaminated")
        self.notebook.add(self.recommendations_tab, text="Recommendations")

        self.inputs = {}
        self.create_general_tab()
        self.create_cracked_tab()
        self.create_burned_tab()
        self.create_undercooked_tab()
        self.create_sized_tab()
        self.create_contaminated_tab()
        self.create_recommendations_tab()

        self.run_button = ttk.Button(self, text="Run Analysis", command=self.run_analysis)
        self.run_button.pack(pady=10)

    def create_general_tab(self):
        questions = self.get_questions_by_category("general")
        for question_id, question_text in questions.items():
            label = ttk.Label(self.general_tab, text=question_text)
            label.pack(anchor="w", padx=10, pady=5)
            entry = ttk.Entry(self.general_tab, width=100)
            entry.pack(anchor="w", padx=10, pady=2, fill="x")
            self.inputs[question_id] = entry

    def create_cracked_tab(self):
        questions = self.get_questions_by_category("cracked")
        for question_id, question_text in questions.items():
            label = ttk.Label(self.cracked_tab, text=question_text)
            label.pack(anchor="w", padx=10, pady=5)
            entry = ttk.Entry(self.cracked_tab, width=100)
            entry.pack(anchor="w", padx=10, pady=2, fill="x")
            self.inputs[question_id] = entry

    def create_burned_tab(self):
        questions = self.get_questions_by_category("burned")
        for question_id, question_text in questions.items():
            label = ttk.Label(self.burned_tab, text=question_text)
            label.pack(anchor="w", padx=10, pady=5)
            entry = ttk.Entry(self.burned_tab, width=100)
            entry.pack(anchor="w", padx=10, pady=2, fill="x")
            self.inputs[question_id] = entry

    def create_undercooked_tab(self):
        questions = self.get_questions_by_category("under_cooked")
        for question_id, question_text in questions.items():
            label = ttk.Label(self.undercooked_tab, text=question_text)
            label.pack(anchor="w", padx=10, pady=5)
            entry = ttk.Entry(self.undercooked_tab, width=100)
            entry.pack(anchor="w", padx=10, pady=2, fill="x")
            self.inputs[question_id] = entry

    def create_sized_tab(self):
        questions = self.get_questions_by_category("sized")
        for question_id, question_text in questions.items():
            label = ttk.Label(self.sized_tab, text=question_text)
            label.pack(anchor="w", padx=10, pady=5)
            entry = ttk.Entry(self.sized_tab, width=100)
            entry.pack(anchor="w", padx=10, pady=2, fill="x")
            self.inputs[question_id] = entry

    def create_contaminated_tab(self):
        questions = self.get_questions_by_category("contaminated")
        for question_id, question_text in questions.items():
            label = ttk.Label(self.contaminated_tab, text=question_text)
            label.pack(anchor="w", padx=10, pady=5)
            entry = ttk.Entry(self.contaminated_tab, width=100)
            entry.pack(anchor="w", padx=10, pady=2, fill="x")
            self.inputs[question_id] = entry

    def create_recommendations_tab(self):
        self.recommendation_text = tk.Text(self.recommendations_tab, wrap="word")
        self.recommendation_text.pack(fill="both", expand=True)

    def get_questions_by_category(self, category):
        questions = {}
        for fact in self.engine.facts.values():
            if isinstance(fact, Question):
                if category == "general" and fact['id'] in ["total", "deffected"]:
                    questions[fact['id']] = fact['text']
                elif category in fact['id']:
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

        self.notebook.select(self.recommendations_tab)

    def get_question_by_id(self, question_id):
        for fact in self.engine.facts.values():
            if isinstance(fact, Question) and fact['id'] == question_id:
                return fact
        return None

if __name__ == "__main__":
    app = App()
    app.mainloop()

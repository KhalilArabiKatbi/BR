import tkinter as tk
from tkinter import messagebox, ttk
from RecommendationEngine import RecommendationEngine
from MyFacts import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quality Control Recommendation System")
        self.geometry("1920x1080")
        self.configure(bg="#1E1E1E")

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

        self.setup_styles()
        self.create_widgets()

        self.ask_next_question()
        self.update_graph()

    def setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#1E1E1E")
        self.style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Segoe UI", 14))
        self.style.configure("TButton", font=("Segoe UI", 12, "bold"), background="#4A90E2", foreground="#FFFFFF")
        self.style.map("TButton", background=[("active", "#357ABD")])
        self.style.configure("TEntry", fieldbackground="#3C3C3C", foreground="#FFFFFF", insertbackground="#FFFFFF")

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for questions and input
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=50, pady=50)

        self.question_label = ttk.Label(left_frame, text="", wraplength=480)
        self.question_label.pack(pady=20)

        self.entry = ttk.Entry(left_frame, font=("Segoe UI", 12), width=50)
        self.entry.pack(pady=10)

        self.submit_button = ttk.Button(left_frame, text="Submit", command=self.submit_answer)
        self.submit_button.pack(pady=10)

        # Right frame for graph and recommendations
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=50, pady=50)

        # Summary Frame
        summary_frame = ttk.Frame(right_frame)
        summary_frame.pack(side=tk.TOP, fill=tk.X, pady=20)

        self.summary_labels = {}
        summary_metrics = ["Total Biscuits", "Total Defected", "Defect Rate"]
        for metric in summary_metrics:
            frame = ttk.Frame(summary_frame)
            frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
            label = ttk.Label(frame, text=metric, font=("Segoe UI", 12, "bold"))
            label.pack()
            value_label = ttk.Label(frame, text="0", font=("Segoe UI", 18))
            value_label.pack()
            self.summary_labels[metric] = value_label

        # Graph
        self.fig = Figure(figsize=(12, 10), dpi=100, facecolor="#1E1E1E")
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Recommendations
        self.recommendation_text = tk.Text(right_frame, wrap="word", height=20, font=("Segoe UI", 14), bg="#3C3C3C", fg="#FFFFFF", borderwidth=0)
        self.recommendation_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.recommendation_text.insert(tk.END, "Recommendations will appear here.")
        self.recommendation_text.config(state="disabled")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

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
            self.update_summary()
            self.update_graph()
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
        recommendations = self.engine.recommendations
        if not recommendations:
            self.recommendation_text.config(state="normal")
            self.recommendation_text.delete(1.0, tk.END)
            self.recommendation_text.insert(tk.END, "No recommendations.")
            self.recommendation_text.config(state="disabled")
        else:
            self.recommendation_text.config(state="normal")
            self.recommendation_text.delete(1.0, tk.END)
            for prediction, recommendation in recommendations:
                self.recommendation_text.insert(tk.END, f"{prediction}\n", ("bold",))
                self.recommendation_text.insert(tk.END, f"{recommendation}\n\n")
            self.recommendation_text.config(state="disabled")

        self.question_label.config(text="Analysis complete. See recommendations.")
        self.entry.pack_forget()
        self.submit_button.pack_forget()

    def update_summary(self):
        total_biscuits = int(self.answers.get("total", 0))
        total_defected = int(self.answers.get("deffected", 0))
        defect_rate = (total_defected / total_biscuits) * 100 if total_biscuits > 0 else 0

        self.summary_labels["Total Biscuits"].config(text=f"{total_biscuits}")
        self.summary_labels["Total Defected"].config(text=f"{total_defected}")
        self.summary_labels["Defect Rate"].config(text=f"{defect_rate:.2f}%")

    def update_graph(self):
        self.fig.clear()
        self.fig.patch.set_facecolor('#1E1E1E')

        gs = self.fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)

        # Donut chart
        ax_donut = self.fig.add_subplot(gs[0, 0])
        self.plot_donut(ax_donut)

        # Bar chart
        ax_bar = self.fig.add_subplot(gs[0, 1])
        self.plot_bar(ax_bar)

        # Sub-plots for defect severity
        ax_cracked = self.fig.add_subplot(gs[1, 0])
        self.plot_severity("cracked", ax_cracked)
        ax_burned = self.fig.add_subplot(gs[1, 1])
        self.plot_severity("burned", ax_burned)

        self.canvas.draw()

    def plot_donut(self, ax):
        ax.set_title("Defect Proportions", color="white", fontsize=16)
        ax.set_facecolor("#1E1E1E")

        defect_counts = {
            "cracked": 0,
            "burned": 0,
            "under_cooked": 0,
            "over_sized": 0,
            "under_sized": 0,
            "contaminated": 0,
        }
        for key, value in self.answers.items():
            if key in defect_counts:
                defect_counts[key] = int(value)

        labels = defect_counts.keys()
        sizes = list(defect_counts.values())
        if sum(sizes) > 0:
            wedges, texts, autotexts = ax.pie(sizes, autopct='%1.1f%%', startangle=140,
                                              colors=plt.cm.Paired.colors, textprops={'color':"w"})
            ax.legend(wedges, labels, title="Defects", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
                      labelcolor='white', facecolor='#3C3C3C', edgecolor='none')
            centre_circle = plt.Circle((0,0),0.70,fc='#1E1E1E')
            ax.add_artist(centre_circle)
        ax.axis('equal')

    def plot_bar(self, ax):
        defect_counts = {
            "cracked": 0,
            "burned": 0,
            "under_cooked": 0,
            "over_sized": 0,
            "under_sized": 0,
            "contaminated": 0,
        }
        for key, value in self.answers.items():
            if key in defect_counts:
                defect_counts[key] = int(value)

        ax.bar(list(defect_counts.keys()), list(defect_counts.values()), color="#4A90E2")
        ax.set_ylabel("Count", color="white", fontsize=12)
        ax.set_title("Defective Biscuits", color="white", fontsize=16)
        ax.tick_params(axis='x', colors='white', rotation=45, labelsize=10)
        ax.tick_params(axis='y', colors='white', labelsize=10)
        ax.set_facecolor("#3C3C3C")
        for spine in ax.spines.values():
            spine.set_edgecolor('white')

    def plot_severity(self, defect_type, ax):
        severities = {
            "severly": 0,
            "moderate": 0,
            "low": 0,
        }
        for key, value in self.answers.items():
            if defect_type in key:
                if "severly" in key:
                    severities["severly"] = int(value)
                elif "moderate" in key:
                    severities["moderate"] = int(value)
                elif "low" in key:
                    severities["low"] = int(value)

        ax.bar(severities.keys(), severities.values(), color=["#FF6384", "#FFCE56", "#36A2EB"])
        ax.set_title(f"{defect_type.capitalize()} Severity", color="white", fontsize=16)
        ax.set_ylabel("Count", color="white", fontsize=12)
        ax.tick_params(axis='x', colors='white', labelsize=10)
        ax.tick_params(axis='y', colors='white', labelsize=10)
        ax.set_facecolor("#3C3C3C")
        for spine in ax.spines.values():
            spine.set_edgecolor('white')

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()

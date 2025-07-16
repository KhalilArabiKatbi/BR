from experta import *
from MyFacts import *


class RecommendationEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.recommendations = []

    @DefFacts()
    def _initial_facts(self):
        yield Fact(init=True)  # Simple initialization fact
        yield Question(
            id="total",
            Type="input_int",
            valid=[],
            text="What is the batch size?",
        )
        yield Question(
            id="deffected",
            Type="input_int",
            valid=[],
            text="how many biscuits are deffected?",
        )
        yield Question(
            id="cracked",
            Type="input_int",
            valid=[],
            text="how many biscuits are cracked?",
        )
        yield Question(
            id="burned",
            Type="input_int",
            valid=[],
            text="how many biscuits are burned?",
        )
        yield Question(
            id="under_cooked",
            Type="input_int",
            valid=[],
            text="how many biscuits are under_cooked?",
        )
        yield Question(
            id="over_sized",
            Type="input_int",
            valid=[],
            text="how many biscuits are over_sized?",
        )
        yield Question(
            id="under_sized",
            Type="input_int",
            valid=[],
            text="how many biscuits are under_sized?",
        )
        yield Question(
            id="contaminated",
            Type="input_int",
            valid=[],
            text="how many biscuits are contaminated?",
        )
        yield Question(
            id="wrong_input",
            Type="input_string",
            valid=[
                "cracked",
                "burned",
                "under_cooked",
                "over_sized",
                "under_sized",
                "contaminated",
            ],
            text="you mistyped one of the deffects number please choose what you put wrong to modify\n1-cracked\n2-burned\n3-under_cooked\n4-over_sized\n5-under_sized\n6-contaminated",
        )
        yield Question(
            id="severly_cracked_count",
            Type="input_int",
            valid=[],
            text="How many severly cracked biscuits (>50%)?",
        )
        yield Question(
            id="moderate_cracked_count",
            Type="input_int",
            valid=[],
            text="How many moderate cracked biscuits (20%~50%)?",
        )
        yield Question(
            id="low_cracked_count",
            Type="input_int",
            valid=[],
            text="How many low cracked biscuits (<20%)?",
        )
        yield Question(
            id="severly_burned_count",
            Type="input_int",
            valid=[],
            text="How many severly burned biscuits (>40%)?",
        )
        yield Question(
            id="moderate_burned_count",
            Type="input_int",
            valid=[],
            text="How many moderate burned biscuits(10%~40%)?",
        )
        yield Question(
            id="low_burned_count",
            Type="input_int",
            valid=[],
            text="How many low burned biscuits(<10%)?",
        )
        yield Question(
            id="severly_under_cooked_count",
            Type="input_int",
            valid=[],
            text="How many severly under_cooked biscuits (>40%)?",
        )
        yield Question(
            id="moderate_under_cooked_count",
            Type="input_int",
            valid=[],
            text="How many moderate under_cooked biscuits(10%~40%)?",
        )
        yield Question(
            id="low_under_cooked_count",
            Type="input_int",
            valid=[],
            text="How many low under_cooked biscuits(<10%)?",
        )
        yield Question(
            id="severly_over_sized_count",
            Type="input_int",
            valid=[],
            text="How many biscuits have raduis greater than 4cm",
        )
        yield Question(
            id="moderate_over_sized_count",
            Type="input_int",
            valid=[],
            text="How many biscuits have raduis between 3.5cm and 4cm?",
        )
        yield Question(
            id="moderate_under_sized_count",
            Type="input_int",
            valid=[],
            text="How many biscuits have raduis between 2.5cm and 3cm?",
        )
        yield Question(
            id="severly_under_sized_count",
            Type="input_int",
            valid=[],
            text="How many biscuits have raduis lower than 2.5cm?",
        )

    @Rule(
        Question(id=MATCH.id, text=MATCH.text, valid=MATCH.valid, Type=MATCH.Type),
        NOT(Answer(id=MATCH.id)),
        AS.ask << Fact(ask=MATCH.id),
    )
    def ask_question_by_id(self, ask, id, text, valid, Type):
        # "Ask a question and assert the answer""
        self.retract(ask)
        answer = self.ask_user(text, Type, valid)
        self.declare(Answer(id=id, text=answer))

    # Useful functions
    def ask_user(self, question, Type, valid=None):
        # "Ask a question, and return the answer"
        answer = ""
        while True:
            print(question)
            answer = input()

            ans = self.is_of_type(answer, Type, valid)
            if ans != None:
                answer = ans
                break

        return answer

    def is_of_type(self, answer, Type, valid):
        # "Check that the answer has the right form"
        ans = answer.strip().replace("%", "")
        if Type == "input_string":
            if ans in valid:
                return ans
        elif Type == "input_int":
            return self.is_a_int(ans)
        elif Type == "input_float":
            return self.is_a_float(ans)
        else:
            return None

    def is_a_int(self, answer):
        try:
            answer = int(answer)
            if answer >= 0:
                return answer
            else:
                return None
        except:
            return None

    def is_a_float(self, answer):
        try:
            answer = float(answer)
            if answer >= 0:
                return answer
            else:
                return None
        except:
            return None

    # Input validation rules
    @Rule(NOT(Answer(id=L("total"))), NOT(Fact(ask=L("total"))))
    def supply_answer_total(self):
        self.declare(Fact(ask="total"))

    @Rule(
        (Answer(id=L("total"))),
        NOT(Answer(id=L("deffected"))),
    )
    def supply_answer_deffected(self):
        self.declare(Fact(ask="deffected"))

    @Rule(
        AS.Def << Answer(id=L("deffected"), text=MATCH.ans1),
        Answer(id=L("total"), text=MATCH.ans2),
        TEST(lambda ans1, ans2: int(ans1) > int(ans2)),
        salience=50,
    )
    def validation1(self, Def):
        self.retract(Def)
        self.declare(Fact(ask="deffected"))

    @Rule(
        (Answer(id=L("deffected"))),
        NOT(Answer(id=L("cracked"))),
    )
    def supply_answer_cracked(self):
        self.declare(Fact(ask="cracked"))

    @Rule(
        (Answer(id=L("cracked"))),
        NOT(Answer(id=L("burned"))),
    )
    def supply_answer_burned(self):
        self.declare(Fact(ask="burned"))

    @Rule(
        (Answer(id=L("burned"))),
        NOT(Answer(id=L("under_cooked"))),
    )
    def supply_answer_under_cooked(self):
        self.declare(Fact(ask="under_cooked"))

    @Rule(
        (Answer(id=L("under_cooked"))),
        NOT(Answer(id=L("over_sized"))),
    )
    def supply_answer_over_sized(self):
        self.declare(Fact(ask="over_sized"))

    @Rule(
        (Answer(id=L("over_sized"))),
        NOT(Answer(id=L("under_sized"))),
    )
    def supply_answer_under_sized(self):
        self.declare(Fact(ask="under_sized"))

    @Rule(
        (Answer(id=L("under_sized"))),
        NOT(Answer(id=L("contaminated"))),
    )
    def supply_answer_contaminated(self):
        self.declare(Fact(ask="contaminated"))

    @Rule(
        Answer(id=L("deffected"), text=MATCH.ans1),
        AS.cr << Answer(id=L("cracked"), text=MATCH.ans2),
        AS.bu << Answer(id=L("burned"), text=MATCH.ans3),
        AS.unc << Answer(id=L("under_cooked"), text=MATCH.ans4),
        AS.ovs << Answer(id=L("over_sized"), text=MATCH.ans5),
        AS.uns << Answer(id=L("under_sized"), text=MATCH.ans6),
        AS.co << Answer(id=L("contaminated"), text=MATCH.ans7),
        TEST(
            lambda ans1, ans2, ans3, ans4, ans5, ans6, ans7: ans1
            < ans2 + ans3 + ans4 + ans5 + ans6 + ans7
        ),
        salience=50,
    )
    def validation2(self, cr, bu, unc, ovs, uns, co):
        self.retract(cr)
        self.retract(bu)
        self.retract(unc)
        self.retract(ovs)
        self.retract(uns)
        self.retract(co)
        self.declare(Fact(ask="cracked"))

    @Rule(
        NOT(Fact(ask="wrong_input")),
        Answer(id=L("deffected"), text=MATCH.ans1),
        Answer(id=L("cracked"), text=MATCH.ans2),
        Answer(id=L("burned"), text=MATCH.ans3),
        Answer(id=L("under_cooked"), text=MATCH.ans4),
        Answer(id=L("over_sized"), text=MATCH.ans5),
        Answer(id=L("under_sized"), text=MATCH.ans6),
        Answer(id=L("contaminated"), text=MATCH.ans7),
        TEST(
            lambda ans1, ans2, ans3, ans4, ans5, ans6, ans7: ans1
            > ans2 + ans3 + ans4 + ans5 + ans6 + ans7
        ),
        salience=50,
    )
    def validation3(self):
        print("validation3")
        self.declare(Fact(ask="wrong_input"))

    @Rule(
        AS.wrong << Answer(id=L("wrong_input"), text=MATCH.id),
        AS.answer << (Answer(id=MATCH.id)),
        salience=100,
    )
    def ReAsk_about_defect_to_modify(self, wrong, answer, id):
        print("ReAsk_about_defect_to_modify")
        self.retract(wrong)
        self.retract(answer)
        self.declare(Fact(ask=id))

    @Rule(
        AS.ans << Answer(id=L("cracked")),
        Answer(id=L("deffected"), text=MATCH.num),
        TEST(lambda ans: "cf" not in ans),
        salience=20,
    )
    def add_cracked_cf(self, ans, num):
        cf = round(ans["text"] / num, 1)
        self.modify(ans, cf=cf)

    @Rule(
        AS.ans << Answer(id=L("burned")),
        Answer(id=L("deffected"), text=MATCH.num),
        TEST(lambda ans: "cf" not in ans),
        salience=20,
    )
    def add_burned_cf(self, ans, num):
        cf = round(ans["text"] / num, 1)
        self.modify(ans, cf=cf)

    @Rule(
        AS.ans << Answer(id=L("under_cooked")),
        Answer(id=L("deffected"), text=MATCH.num),
        TEST(lambda ans: "cf" not in ans),
        salience=20,
    )
    def add_under_cooked_cf(self, ans, num):
        cf = round(ans["text"] / num, 1)
        self.modify(ans, cf=cf)

    @Rule(
        AS.ans << Answer(id=L("over_sized")),
        Answer(id=L("deffected"), text=MATCH.num),
        TEST(lambda ans: "cf" not in ans),
        salience=20,
    )
    def add_over_sized_cf(self, ans, num):
        cf = round(ans["text"] / num, 1)
        self.modify(ans, cf=cf)

    @Rule(
        AS.ans << Answer(id=L("under_sized")),
        Answer(id=L("deffected"), text=MATCH.num),
        TEST(lambda ans: "cf" not in ans),
        salience=20,
    )
    def add_under_sized_cf(self, ans, num):
        cf = round(ans["text"] / num, 1)
        self.modify(ans, cf=cf)

    @Rule(
        AS.ans << Answer(id=L("contaminated")),
        Answer(id=L("deffected"), text=MATCH.num),
        TEST(lambda ans: "cf" not in ans),
        salience=20,
    )
    def add_contaminated_cf(self, ans, num):
        cf = round(ans["text"] / num, 1)
        self.modify(ans, cf=cf)

    # the rules for each deffect
    @Rule(
        (Answer(id=L("contaminated"))),
        NOT(Answer(id=L("severly_cracked_count"))),
    )
    def supply_answer_severe_cracked_count(self):
        self.declare(Fact(ask="severly_cracked_count"))

    @Rule(
        (Answer(id=L("severly_cracked_count"))),
        NOT(Answer(id=L("moderate_cracked_count"))),
    )
    def supply_answer_moderate_cracked_count(self):
        self.declare(Fact(ask="moderate_cracked_count"))

    @Rule(
        (Answer(id=L("moderate_cracked_count"))),
        NOT(Answer(id=L("low_cracked_count"))),
    )
    def supply_answer_low_cracked_count(self):
        self.declare(Fact(ask="low_cracked_count"))

    Rule(
        (Answer(id=L("cracked"), text=MATCH.ans1)),
        (AS.se << Answer(id=L("severly_cracked_count"), text=MATCH.ans2)),
        (AS.mo << Answer(id=L("moderate_cracked_count"), text=MATCH.ans3)),
        (AS.lo << Answer(id=L("low_cracked_count"), text=MATCH.ans4)),
        TEST(lambda ans1, ans2, ans3, ans4: ans1 != ans2 + ans3 + ans4),
        salience=50,
    )

    def validate_cracked_num(self, se, mo, lo):
        self.retract(se)
        self.retract(mo)
        self.retract(lo)
        self.declare(Fact(ask="severly_cracked_count"))

    @Rule(
        (Answer(id=L("low_cracked_count"))),
        NOT(Answer(id=L("severly_burned_count"))),
    )
    def supply_answer_severe_burned_count(self):
        self.declare(Fact(ask="severly_burned_count"))

    @Rule(
        (Answer(id=L("severly_burned_count"))),
        NOT(Answer(id=L("moderate_burned_count"))),
    )
    def supply_answer_moderate_burned_count(self):
        self.declare(Fact(ask="moderate_burned_count"))

    @Rule(
        (Answer(id=L("moderate_burned_count"))),
        NOT(Answer(id=L("low_burned_count"))),
    )
    def supply_answer_low_burned_count(self):
        self.declare(Fact(ask="low_burned_count"))

    Rule(
        (Answer(id=L("burned"), text=MATCH.ans1)),
        (AS.se << Answer(id=L("severly_burned_count"), text=MATCH.ans2)),
        (AS.mo << Answer(id=L("moderate_burned_count"), text=MATCH.ans3)),
        (AS.lo << Answer(id=L("low_burned_count"), text=MATCH.ans4)),
        TEST(lambda ans1, ans2, ans3, ans4: ans1 != ans2 + ans3 + ans4),
        salience=50,
    )

    def validate_burned_num(self, se, mo, lo):
        self.retract(se)
        self.retract(mo)
        self.retract(lo)
        self.declare(Fact(ask="severly_burned_count"))

    @Rule(
        (Answer(id=L("low_burned_count"))),
        NOT(Answer(id=L("severly_under_cooked_count"))),
    )
    def supply_answer_severe_under_cooked_count(self):
        self.declare(Fact(ask="severly_under_cooked_count"))

    @Rule(
        (Answer(id=L("severly_under_cooked_count"))),
        NOT(Answer(id=L("moderate_under_cooked_count"))),
    )
    def supply_answer_moderate_under_cooked_count(self):
        self.declare(Fact(ask="moderate_under_cooked_count"))

    @Rule(
        (Answer(id=L("moderate_under_cooked_count"))),
        NOT(Answer(id=L("low_under_cooked_count"))),
    )
    def supply_answer_low_under_cooked_count(self):
        self.declare(Fact(ask="low_under_cooked_count"))

    Rule(
        (Answer(id=L("under_cooked"), text=MATCH.ans1)),
        (AS.se << Answer(id=L("severly_under_cooked_count"), text=MATCH.ans2)),
        (AS.mo << Answer(id=L("moderate_under_cooked_count"), text=MATCH.ans3)),
        (AS.lo << Answer(id=L("low_under_cooked_count"), text=MATCH.ans4)),
        TEST(lambda ans1, ans2, ans3, ans4: ans1 != ans2 + ans3 + ans4),
        salience=50,
    )

    def validate_under_cooked_num(self, se, mo, lo):
        self.retract(se)
        self.retract(mo)
        self.retract(lo)
        self.declare(Fact(ask="severly_under_cooked_count"))

    @Rule(
        (Answer(id=L("low_under_cooked_count"))),
        NOT(Answer(id=L("severly_over_sized_count"))),
    )
    def supply_answer_severly_over_sized_count(self):
        self.declare(Fact(ask="severly_over_sized_count"))

    @Rule(
        (Answer(id=L("severly_over_sized_count"))),
        NOT(Answer(id=L("moderate_over_sized_count"))),
    )
    def supply_answer_moderate_over_sized_count(self):
        self.declare(Fact(ask="moderate_over_sized_count"))

    Rule(
        (Answer(id=L("over_sized"), text=MATCH.ans1)),
        (AS.se << Answer(id=L("severly_over_sized_count"), text=MATCH.ans2)),
        (AS.mo << Answer(id=L("moderate_over_sized_count"), text=MATCH.ans3)),
        TEST(lambda ans1, ans2, ans3: ans1 != ans2 + ans3),
        salience=50,
    )

    def validate_over_sized_num(self, se, mo):
        self.retract(se)
        self.retract(mo)
        self.declare(Fact(ask="severly_over_sized_count"))

    @Rule(
        (Answer(id=L("moderate_over_sized_count"))),
        NOT(Answer(id=L("severly_under_sized_count"))),
    )
    def supply_answer_severly_under_sized_count(self):
        self.declare(Fact(ask="severly_under_sized_count"))

    @Rule(
        (Answer(id=L("severly_under_sized_count"))),
        NOT(Answer(id=L("moderate_under_sized_count"))),
    )
    def supply_answer_moderate_under_sized_count(self):
        self.declare(Fact(ask="moderate_under_sized_count"))

    Rule(
        (Answer(id=L("under_sized"), text=MATCH.ans1)),
        (AS.se << Answer(id=L("severly_under_sized_count"), text=MATCH.ans2)),
        (AS.mo << Answer(id=L("moderate_under_sized_count"), text=MATCH.ans3)),
        TEST(lambda ans1, ans2, ans3: ans1 != ans2 + ans3),
        salience=50,
    )

    def validate_under_sized_num(self, se, mo):
        self.retract(se)
        self.retract(mo)
        self.declare(Fact(ask="severly_under_sized_count"))

    # Declaring the rules that declares deffects
    @Rule(
        (Answer(id=L("cracked"), text=MATCH.cr, cf=MATCH.cf)),
        (Answer(id=L("severly_cracked_count"), text=MATCH.se)),
        (Answer(id=L("moderate_cracked_count"), text=MATCH.mo)),
        (Answer(id=L("low_cracked_count"), text=MATCH.lo)),
    )
    def declare_cracked(self, cr, cf, se, mo, lo):
        severity_factor = ((se * 0.8) + (mo * 0.5) + (lo * 0.1)) / cr
        new_cf = cf * severity_factor
        self.declare(Cracked(cf=new_cf))

    @Rule(
        (Answer(id=L("burned"), text=MATCH.cr, cf=MATCH.cf)),
        (Answer(id=L("severly_burned_count"), text=MATCH.se)),
        (Answer(id=L("moderate_burned_count"), text=MATCH.mo)),
        (Answer(id=L("low_burned_count"), text=MATCH.lo)),
    )
    def declare_burned(self, br, cf, se, mo, lo):
        severity_factor = ((se * 0.8) + (mo * 0.5) + (lo * 0.1)) / br
        new_cf = cf * severity_factor
        self.declare(Burned(cf=new_cf))

    @Rule(
        (Answer(id=L("under_cooked"), text=MATCH.uc, cf=MATCH.cf)),
        (Answer(id=L("severly_under_cooked_count"), text=MATCH.se)),
        (Answer(id=L("moderate_under_cooked_count"), text=MATCH.mo)),
        (Answer(id=L("low_under_cooked_count"), text=MATCH.lo)),
    )
    def declare_under_cooked(self, uc, cf, se, mo, lo):
        severity_factor = ((se * 0.8) + (mo * 0.5) + (lo * 0.1)) / uc
        new_cf = cf * severity_factor
        self.declare(UnderCooked(cf=new_cf))

    @Rule(
        (Answer(id=L("over_sized"), text=MATCH.os, cf=MATCH.cf)),
        (Answer(id=L("severly_over_sized_count"), text=MATCH.se)),
        (Answer(id=L("moderate_over_sized_count"), text=MATCH.mo)),
    )
    def declare_over_sized(self, os, cf, se, mo):
        severity_factor = ((se * 0.8) + (mo * 0.5)) / os
        new_cf = cf * severity_factor
        self.declare(OverSized(cf=new_cf))

    @Rule(
        (Answer(id=L("under_sized"), text=MATCH.us, cf=MATCH.cf)),
        (Answer(id=L("severly_under_sized_count"), text=MATCH.se)),
        (Answer(id=L("moderate_under_sized_count"), text=MATCH.mo)),
    )
    def declare_under_sized(self, us, cf, se, mo):
        severity_factor = ((se * 0.8) + (mo * 0.5)) / us
        new_cf = cf * severity_factor
        self.declare(UnderSized(cf=new_cf))

    @Rule((Answer(id=L("contaminated"))), salience=20)
    def declare_under_sized(self):
        self.declare(Contaminated())

    @Rule(
        (Answer(id=L("total"), text=MATCH.tnum)),
        (Answer(id=L("deffected"), text=MATCH.dnum)),
        TEST(lambda tnum, dnum: dnum > tnum // 3),
    )
    def critical_deffected(self):
        print("critical_deffected")
        pass

    # Cracked rules
    @Rule(Answer(id=L("cracked"), cf=MATCH.cf), Cracked(size=P(lambda x: x >= 20)))
    def critical_cracked(self, cf):
        self.declare(
            Prediction(
                text="Conveyor or dough - critical cracking (≥20% cracked)", cf=cf
            )
        )

    @Rule(Answer(id=L("cracked"), cf=MATCH.cf), Cracked(size=P(lambda x: 5 <= x < 20)))
    def moderate_cracked(self, cf):
        self.declare(Prediction(text="Conveyor speed - (5~20% cracked)", cf=cf))

    @Rule(Answer(id=L("cracked"), cf=MATCH.cf), Cracked(size=P(lambda x: x < 5)))
    def minor_cracked(self, cf):
        self.declare(Prediction(text="Normal wear - (<5% cracked)", cf=cf))

    # Burned rules
    @Rule(Answer(id=L("burned"), cf=MATCH.cf), Burned(percentage=P(lambda x: x >= 15)))
    def critical_burned(self, cf):
        self.declare(
            Prediction(
                text="Malfunctional Oven - critical burning (≥15% burned)", cf=cf
            )
        )

    @Rule(
        Answer(id=L("burned"), cf=MATCH.cf), Burned(percentage=P(lambda x: 3 <= x < 15))
    )
    def moderate_burned(self, cf):
        self.declare(
            Prediction(
                text="Malfunctional thermocouple or wrong settings - (3~15% burned)",
                cf=cf,
            )
        )

    # UnderCooked rules
    @Rule(
        Answer(id=L("under_cooked"), cf=MATCH.cf),
        UnderCooked(percentage=P(lambda x: x >= 10)),
    )
    def critical_undercooked(self, cf):
        self.declare(
            Prediction(
                text="Malfunctional Oven - critical undercook - (≥10% undercooked)",
                cf=cf,
            )
        )

    @Rule(
        Answer(id=L("under_cooked"), cf=MATCH.cf),
        UnderCooked(percentage=P(lambda x: x < 10)),
    )
    def acceptable_undercooked(self, cf):
        self.declare(
            Prediction(
                text="Malfunctional thermocouple or wrong settings - (<10% undercooked)",
                cf=cf,
            )
        )

    # Size-related rules
    @Rule(Answer(id=L("overe_sized"), cf=MATCH.cf), OverSized(size=P(lambda x: x > 15)))
    def critical_oversized(self, cf):
        self.declare(
            Prediction(
                text="Mold cutter deformed critical - (>15)",
                cf=cf,
            )
        )

    @Rule(
        Answer(id=L("overe_sized"), cf=MATCH.cf),
        OverSized(size=P(lambda x: 12 <= x <= 15)),
    )
    def moderate_oversized(self, cf):
        self.declare(
            Prediction(
                text="Mold cutter deformed slightly - (12~15)",
                cf=cf,
            )
        )

    @Rule(
        Answer(id=L("under_sized"), cf=MATCH.cf),
        UnderSized(size=P(lambda x: 10 <= x <= 12)),
    )
    def moderate_undersized(self, cf):
        self.declare(
            Prediction(
                text="Mold cutter deformed slightly - (10~12)",
                cf=cf,
            )
        )

    @Rule(
        Answer(id=L("under_sized"), cf=MATCH.cf), UnderSized(size=P(lambda x: x < 10))
    )
    def critical_undersized(self, cf):
        self.declare(
            Prediction(
                text="Mold cutter deformed slightly - (<10)",
                cf=cf,
            )
        )

    # Contamination rule
    @Rule(Contaminated(), salience=1000)
    def force_reject(self):
        self.declare(Fact(recommendation="CRITICAL: Foreign object found in dough"))

    # Collect recommendations
    @Rule(Fact(recommendation=MATCH.r), salience=-1000)
    def collect_recommendation(self, r):
        if r not in self.recommendations:
            self.recommendations.append(r)

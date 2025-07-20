from collections.abc import Mapping
from experta import *
from MyFacts import *


class RecommendationEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.recommendations = []

    @DefFacts()
    def _initial_facts(self):
        yield Fact(init=True)
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
            id="severely_cracked_count",
            Type="input_int",
            valid=[],
            text="How many severely cracked biscuits (>50%)?",
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
            id="severely_burned_count",
            Type="input_int",
            valid=[],
            text="How many severely burned biscuits (>40%)?",
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
            id="severely_under_cooked_count",
            Type="input_int",
            valid=[],
            text="How many severely under_cooked biscuits (>40%)?",
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
            id="severely_over_sized_count",
            Type="input_int",
            valid=[],
            text="How many biscuits have radius greater than 4cm",
        )
        yield Question(
            id="moderate_over_sized_count",
            Type="input_int",
            valid=[],
            text="How many biscuits have radius between 3.5cm and 4cm?",
        )
        yield Question(
            id="moderate_under_sized_count",
            Type="input_int",
            valid=[],
            text="How many biscuits have radius between 2.5cm and 3cm?",
        )
        yield Question(
            id="severely_under_sized_count",
            Type="input_int",
            valid=[],
            text="How many biscuits have radius lower than 2.5cm?",
        )


    # Input validation rules
    @Rule(NOT(Answer(id=L("total"))), NOT(Fact(ask=L("total"))))
    def supply_answer_total(self):
        self.declare(Fact(ask="total"))

    @Rule(
        AS.ans << Answer(id=L("total"), text=MATCH.tot),
        TEST(lambda tot: int(tot) == 0),
        NOT(Answer(id=L("deffected"))),
        salience=55,
    )
    def invalid_total(self, ans):
        self.retract(ans)
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
            lambda ans1, ans2, ans3, ans4, ans5, ans6, ans7: int(ans1)
            < int(ans2) + int(ans3) + int(ans4) + int(ans5) + int(ans6) + int(ans7)
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
            lambda ans1, ans2, ans3, ans4, ans5, ans6, ans7: int(ans1)
            > int(ans2) + int(ans3) + int(ans4) + int(ans5) + int(ans6) + int(ans7)
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
        if int(num) == 0:
            cf = 0.0
        else:
            cf = round(int(ans["text"]) / int(num), 1)
        self.modify(ans, cf=cf)

    @Rule(
        AS.ans << Answer(id=L("burned")),
        Answer(id=L("deffected"), text=MATCH.num),
        TEST(lambda ans: "cf" not in ans),
        salience=20,
    )
    def add_burned_cf(self, ans, num):
        if int(num) == 0:
            cf = 0.0
        else:
            cf = round(int(ans["text"]) / int(num), 1)
        self.modify(ans, cf=cf)

    @Rule(
        AS.ans << Answer(id=L("under_cooked")),
        Answer(id=L("deffected"), text=MATCH.num),
        TEST(lambda ans: "cf" not in ans),
        salience=20,
    )
    def add_under_cooked_cf(self, ans, num):
        if int(num) == 0:
            cf = 0.0
        else:
            cf = round(int(ans["text"]) / int(num), 1)
        self.modify(ans, cf=cf)

    @Rule(
        AS.ans << Answer(id=L("over_sized")),
        Answer(id=L("deffected"), text=MATCH.num),
        TEST(lambda ans: "cf" not in ans),
        salience=20,
    )
    def add_over_sized_cf(self, ans, num):
        if int(num) == 0:
            cf = 0.0
        else:
            cf = round(int(ans["text"]) / int(num), 1)
        self.modify(ans, cf=cf)

    @Rule(
        AS.ans << Answer(id=L("under_sized")),
        Answer(id=L("deffected"), text=MATCH.num),
        TEST(lambda ans: "cf" not in ans),
        salience=20,
    )
    def add_under_sized_cf(self, ans, num):
        if int(num) == 0:
            cf = 0.0
        else:
            cf = round(int(ans["text"]) / int(num), 1)
        self.modify(ans, cf=cf)

    @Rule(
        AS.ans << Answer(id=L("contaminated")),
        Answer(id=L("deffected"), text=MATCH.num),
        TEST(lambda ans: "cf" not in ans),
        salience=20,
    )
    def add_contaminated_cf(self, ans, num):
        if int(num) == 0:
            cf = 0.0
        else:
            cf = round(int(ans["text"]) / int(num), 1)
        self.modify(ans, cf=cf)

    # the rules for each deffect
    @Rule(
        (Answer(id=L("contaminated"))),
        NOT(Answer(id=L("severely_cracked_count"))),
    )
    def supply_answer_severe_cracked_count(self):
        self.declare(Fact(ask="severely_cracked_count"))

    @Rule(
        (Answer(id=L("severely_cracked_count"))),
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

    @Rule(
        (Answer(id=L("cracked"), text=MATCH.ans1)),
        (AS.se << Answer(id=L("severely_cracked_count"), text=MATCH.ans2)),
        (AS.mo << Answer(id=L("moderate_cracked_count"), text=MATCH.ans3)),
        (AS.lo << Answer(id=L("low_cracked_count"), text=MATCH.ans4)),
        TEST(
            lambda ans1, ans2, ans3, ans4: int(ans1)
            != int(ans2) + int(ans3) + int(ans4)
        ),
        salience=50,
    )
    def validate_cracked_num(self, se, mo, lo):
        self.retract(se)
        self.retract(mo)
        self.retract(lo)
        self.declare(Fact(ask="severely_cracked_count"))

    @Rule(
        (Answer(id=L("low_cracked_count"))),
        NOT(Answer(id=L("severely_burned_count"))),
    )
    def supply_answer_severe_burned_count(self):
        self.declare(Fact(ask="severely_burned_count"))

    @Rule(
        (Answer(id=L("severely_burned_count"))),
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

    @Rule(
        (Answer(id=L("burned"), text=MATCH.ans1)),
        (AS.se << Answer(id=L("severely_burned_count"), text=MATCH.ans2)),
        (AS.mo << Answer(id=L("moderate_burned_count"), text=MATCH.ans3)),
        (AS.lo << Answer(id=L("low_burned_count"), text=MATCH.ans4)),
        TEST(
            lambda ans1, ans2, ans3, ans4: int(ans1)
            != int(ans2) + int(ans3) + int(ans4)
        ),
        salience=50,
    )
    def validate_burned_num(self, se, mo, lo):
        self.retract(se)
        self.retract(mo)
        self.retract(lo)
        self.declare(Fact(ask="severely_burned_count"))

    @Rule(
        (Answer(id=L("low_burned_count"))),
        NOT(Answer(id=L("severely_under_cooked_count"))),
    )
    def supply_answer_severe_under_cooked_count(self):
        self.declare(Fact(ask="severely_under_cooked_count"))

    @Rule(
        (Answer(id=L("severely_under_cooked_count"))),
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

    @Rule(
        (Answer(id=L("under_cooked"), text=MATCH.ans1)),
        (AS.se << Answer(id=L("severely_under_cooked_count"), text=MATCH.ans2)),
        (AS.mo << Answer(id=L("moderate_under_cooked_count"), text=MATCH.ans3)),
        (AS.lo << Answer(id=L("low_under_cooked_count"), text=MATCH.ans4)),
        TEST(
            lambda ans1, ans2, ans3, ans4: int(ans1)
            != int(ans2) + int(ans3) + int(ans4)
        ),
        salience=50,
    )
    def validate_under_cooked_num(self, se, mo, lo):
        self.retract(se)
        self.retract(mo)
        self.retract(lo)
        self.declare(Fact(ask="severely_under_cooked_count"))

    @Rule(
        (Answer(id=L("low_under_cooked_count"))),
        NOT(Answer(id=L("severely_over_sized_count"))),
    )
    def supply_answer_severly_over_sized_count(self):
        self.declare(Fact(ask="severely_over_sized_count"))

    @Rule(
        (Answer(id=L("severely_over_sized_count"))),
        NOT(Answer(id=L("moderate_over_sized_count"))),
    )
    def supply_answer_moderate_over_sized_count(self):
        self.declare(Fact(ask="moderate_over_sized_count"))

    @Rule(
        (Answer(id=L("over_sized"), text=MATCH.ans1)),
        (AS.se << Answer(id=L("severely_over_sized_count"), text=MATCH.ans2)),
        (AS.mo << Answer(id=L("moderate_over_sized_count"), text=MATCH.ans3)),
        TEST(lambda ans1, ans2, ans3: int(ans1) != int(ans2) + int(ans3)),
        salience=50,
    )
    def validate_over_sized_num(self, se, mo):
        self.retract(se)
        self.retract(mo)
        self.declare(Fact(ask="severely_over_sized_count"))

    @Rule(
        (Answer(id=L("moderate_over_sized_count"))),
        NOT(Answer(id=L("severely_under_sized_count"))),
    )
    def supply_answer_severly_under_sized_count(self):
        self.declare(Fact(ask="severely_under_sized_count"))

    @Rule(
        (Answer(id=L("severely_under_sized_count"))),
        NOT(Answer(id=L("moderate_under_sized_count"))),
    )
    def supply_answer_moderate_under_sized_count(self):
        self.declare(Fact(ask="moderate_under_sized_count"))

    @Rule(
        (Answer(id=L("under_sized"), text=MATCH.ans1)),
        (AS.se << Answer(id=L("severely_under_sized_count"), text=MATCH.ans2)),
        (AS.mo << Answer(id=L("moderate_under_sized_count"), text=MATCH.ans3)),
        TEST(lambda ans1, ans2, ans3: int(ans1) != int(ans2) + int(ans3)),
        salience=50,
    )
    def validate_under_sized_num(self, se, mo):
        self.retract(se)
        self.retract(mo)
        self.declare(Fact(ask="severely_under_sized_count"))

    # Declaring the rules that declares deffects
    @Rule(
        Answer(id=L("cracked"), text=MATCH.cr, cf=MATCH.cf),
        Answer(id=L("total"), text=MATCH.tot),
        Answer(id=L("severely_cracked_count"), text=MATCH.se),
        Answer(id=L("moderate_cracked_count"), text=MATCH.mo),
        Answer(id=L("low_cracked_count"), text=MATCH.lo),
        TEST(lambda cr: int(cr) > 0),
    )
    def declare_cracked(self, cr, tot, cf, se, mo, lo):
        percentage = (int(cr) / int(tot)) * 100
        severity_factor = (int(se) * 0.8 + int(mo) * 0.5 + int(lo) * 0.1) / int(cr)
        new_cf = cf * severity_factor
        self.declare(Cracked(percentage=percentage, cf=new_cf))

    @Rule(
        Answer(id=L("burned"), text=MATCH.br, cf=MATCH.cf),
        Answer(id=L("total"), text=MATCH.tot),
        Answer(id=L("severely_burned_count"), text=MATCH.se),
        Answer(id=L("moderate_burned_count"), text=MATCH.mo),
        Answer(id=L("low_burned_count"), text=MATCH.lo),
        TEST(lambda br: int(br) > 0),
    )
    def declare_burned(self, br, tot, cf, se, mo, lo):
        percentage = (int(br) / int(tot)) * 100
        severity_factor = (int(se) * 0.8 + int(mo) * 0.5 + int(lo) * 0.1) / int(br)
        new_cf = cf * severity_factor
        self.declare(Burned(percentage=percentage, cf=new_cf))

    @Rule(
        Answer(id=L("under_cooked"), text=MATCH.uc, cf=MATCH.cf),
        Answer(id=L("total"), text=MATCH.tot),
        Answer(id=L("severely_under_cooked_count"), text=MATCH.se),
        Answer(id=L("moderate_under_cooked_count"), text=MATCH.mo),
        Answer(id=L("low_under_cooked_count"), text=MATCH.lo),
        TEST(lambda uc: int(uc) > 0),
    )
    def declare_under_cooked(self, uc, tot, cf, se, mo, lo):
        percentage = (int(uc) / int(tot)) * 100
        severity_factor = (int(se) * 0.8 + int(mo) * 0.5 + int(lo) * 0.1) / int(uc)
        new_cf = cf * severity_factor
        self.declare(UnderCooked(percentage=percentage, cf=new_cf))

    @Rule(
        Answer(id=L("over_sized"), text=MATCH.os, cf=MATCH.cf),
        Answer(id=L("total"), text=MATCH.tot),
        Answer(id=L("severely_over_sized_count"), text=MATCH.se),
        Answer(id=L("moderate_over_sized_count"), text=MATCH.mo),
        TEST(lambda os: int(os) > 0),
    )
    def declare_over_sized(self, os, tot, cf, se, mo):
        percentage = (int(os) / int(tot)) * 100
        severity_factor = (int(se) * 0.8 + int(mo) * 0.5) / int(os)
        new_cf = cf * severity_factor
        self.declare(OverSized(percentage=percentage, cf=new_cf))

    @Rule(
        Answer(id=L("under_sized"), text=MATCH.us, cf=MATCH.cf),
        Answer(id=L("total"), text=MATCH.tot),
        Answer(id=L("severely_under_sized_count"), text=MATCH.se),
        Answer(id=L("moderate_under_sized_count"), text=MATCH.mo),
        TEST(lambda us: int(us) > 0),
    )
    def declare_under_sized(self, us, tot, cf, se, mo):
        percentage = (int(us) / int(tot)) * 100
        severity_factor = (int(se) * 0.8 + int(mo) * 0.5) / int(us)
        new_cf = cf * severity_factor
        self.declare(UnderSized(percentage=percentage, cf=new_cf))

    @Rule(
        Answer(id=L("contaminated"), text=MATCH.con, cf=MATCH.cf),
        Answer(id=L("total"), text=MATCH.tot),
        TEST(lambda con: int(con) > 0),
        salience=20,
    )
    def declare_contaminated(self, con, tot, cf):
        percentage = (int(con) / int(tot)) * 100
        new_cf = cf
        self.declare(Contaminated(percentage=percentage, cf=new_cf))

    @Rule(
        Answer(id=L("total"), text=MATCH.tnum),
        Answer(id=L("deffected"), text=MATCH.dnum),
        TEST(lambda tnum, dnum: int(dnum) > int(tnum) // 3),
    )
    def critical_deffected(self, tnum, dnum):
        if int(tnum) == 0:
            cf = 0.0
        else:
            cf = round(int(dnum) / int(tnum), 1)
        self.declare(Prediction(text="Critical overall defects (>33% defected)", cf=cf))
        self.declare(
            Fact(
                recommendation="- Furnace: Inspect for general malfunctions if burn/undercook dominate.\n- Dough: Inspect formula and mixing if cracking/contamination dominate.\n- The line: Full audit and maintenance if cracking/size issues dominate.\n- Iron appendages: Inspect for contamination sources if applicable.\n- Mold cutter: Inspect for deformation if size issues dominate."
            )
        )

    # Cracked rules
    @Rule(Cracked(percentage=P(lambda x: x >= 20), cf=MATCH.cf))
    def critical_cracked(self, cf):
        self.declare(
            Prediction(
                text="Conveyor or dough - critical cracking (≥20% cracked)", cf=cf
            )
        )
        self.declare(
            Fact(
                recommendation="- Furnace: No action.\n- Dough: Inspect for improper mixing or low moisture; adjust formula to improve elasticity and reduce cracking.\n- The line: Inspect conveyor belt for damage, misalignment, or excessive vibration; repair or replace sections.\n- Iron appendages: No action.\n- Mold cutter: No action."
            )
        )

    @Rule(Cracked(percentage=P(lambda x: 5 <= x < 20), cf=MATCH.cf))
    def moderate_cracked(self, cf):
        self.declare(Prediction(text="Conveyor speed - (5~20% cracked)", cf=cf))
        self.declare(
            Fact(
                recommendation="- Furnace: No action.\n- Dough: No action.\n- The line: Adjust conveyor speed to ensure even baking and reduce stress on biscuits; calibrate motors.\n- Iron appendages: No action.\n- Mold cutter: No action."
            )
        )

    @Rule(Cracked(percentage=P(lambda x: x < 5), cf=MATCH.cf))
    def minor_cracked(self, cf):
        self.declare(Prediction(text="Normal wear - (<5% cracked)", cf=cf))
        self.declare(
            Fact(
                recommendation="- Furnace: No action.\n- Dough: No action.\n- The line: Monitor for ongoing wear; no immediate action needed.\n- Iron appendages: No action.\n- Mold cutter: No action."
            )
        )

    # Burned rules
    @Rule(Burned(percentage=P(lambda x: x >= 15), cf=MATCH.cf))
    def critical_burned(self, cf):
        self.declare(
            Prediction(
                text="Malfunctional Oven - critical burning (≥15% burned)", cf=cf
            )
        )
        self.declare(
            Fact(
                recommendation="- Furnace: Inspect for heating element failure or uneven heat distribution; repair or replace oven.\n- Dough: No action.\n- The line: No action.\n- Iron appendages: No action.\n- Mold cutter: No action."
            )
        )

    @Rule(Burned(percentage=P(lambda x: 3 <= x < 15), cf=MATCH.cf))
    def moderate_burned(self, cf):
        self.declare(
            Prediction(
                text="Malfunctional thermocouple or wrong settings - (3~15% burned)",
                cf=cf,
            )
        )
        self.declare(
            Fact(
                recommendation="- Furnace: Check and calibrate thermocouple; adjust temperature settings for even baking.\n- Dough: No action.\n- The line: No action.\n- Iron appendages: No action.\n- Mold cutter: No action."
            )
        )

    # UnderCooked rules
    @Rule(UnderCooked(percentage=P(lambda x: x >= 10), cf=MATCH.cf))
    def critical_undercooked(self, cf):
        self.declare(
            Prediction(
                text="Malfunctional Oven - critical undercook - (≥10% undercooked)",
                cf=cf,
            )
        )
        self.declare(
            Fact(
                recommendation="- Furnace: Inspect for heating failure or low temperature output; repair or replace oven.\n- Dough: No action.\n- The line: No action.\n- Iron appendages: No action.\n- Mold cutter: No action."
            )
        )

    @Rule(UnderCooked(percentage=P(lambda x: x < 10), cf=MATCH.cf))
    def acceptable_undercooked(self, cf):
        self.declare(
            Prediction(
                text="Malfunctional thermocouple or wrong settings - (<10% undercooked)",
                cf=cf,
            )
        )
        self.declare(
            Fact(
                recommendation="- Furnace: Check and calibrate thermocouple; increase temperature settings slightly.\n- Dough: No action.\n- The line: No action.\n- Iron appendages: No action.\n- Mold cutter: No action."
            )
        )

    # Size-related rules
    @Rule(OverSized(percentage=P(lambda x: x > 15), cf=MATCH.cf))
    def critical_oversized(self, cf):
        self.declare(
            Prediction(
                text="Mold cutter deformed critical - (>15% oversized)",
                cf=cf,
            )
        )
        self.declare(
            Fact(
                recommendation="- Furnace: No action.\n- Dough: No action.\n- The line: No action.\n- Iron appendages: No action.\n- Mold cutter: Inspect for major deformation; replace cutter immediately."
            )
        )

    @Rule(OverSized(percentage=P(lambda x: 12 <= x <= 15), cf=MATCH.cf))
    def moderate_oversized(self, cf):
        self.declare(
            Prediction(
                text="Mold cutter deformed slightly - (12~15% oversized)",
                cf=cf,
            )
        )
        self.declare(
            Fact(
                recommendation="- Furnace: No action.\n- Dough: No action.\n- The line: No action.\n- Iron appendages: No action.\n- Mold cutter: Inspect for minor wear; repair or realign cutter."
            )
        )

    @Rule(UnderSized(percentage=P(lambda x: x >= 15), cf=MATCH.cf))
    def critical_undersized(self, cf):
        self.declare(
            Prediction(
                text="Mold cutter deformed critical - (>=15% undersized)",
                cf=cf,
            )
        )
        self.declare(
            Fact(
                recommendation="- Furnace: No action.\n- Dough: No action.\n- The line: No action.\n- Iron appendages: No action.\n- Mold cutter: Inspect for major deformation; replace cutter immediately."
            )
        )

    @Rule(UnderSized(percentage=P(lambda x: 10 <= x < 15), cf=MATCH.cf))
    def moderate_undersized(self, cf):
        self.declare(
            Prediction(
                text="Mold cutter deformed slightly - (10~15% undersized)",
                cf=cf,
            )
        )
        self.declare(
            Fact(
                recommendation="- Furnace: No action.\n- Dough: No action.\n- The line: No action.\n- Iron appendages: No action.\n- Mold cutter: Inspect for minor wear; repair or realign cutter."
            )
        )

    # Contamination rule
    @Rule(Contaminated(cf=MATCH.cf), salience=1000)
    def force_reject(self, cf):
        self.declare(Prediction(text="CRITICAL: Foreign object found in dough", cf=cf))
        self.declare(
            Fact(
                recommendation="- Furnace: No action.\n- Dough: Halt production; discard affected batch and screen ingredients for contaminants.\n- The line: Full inspection and cleaning of entire production line to remove loose parts.\n- Iron appendages: If the line has iron appendages, inspect for rust, loose bolts, or metal fragments; remove or secure them to prevent further contamination.\n- Mold cutter: No action."
            )
        )

    # Collect recommendations
    @Rule(Fact(recommendation=MATCH.r), salience=-1000)
    def collect_recommendation(self, r):
        if r not in self.recommendations:
            self.recommendations.append(r)
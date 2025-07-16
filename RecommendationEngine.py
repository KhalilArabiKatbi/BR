from experta import *
from MyFacts import *


class RecommendationEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.recommendations = []

    @DefFacts()
    def _initial_facts(self):
        yield Fact(init=True)

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
    def declare_contaminated(self):
        self.declare(Contaminated())

    @Rule(
        (Answer(id=L("total"), text=MATCH.tnum)),
        (Answer(id=L("deffected"), text=MATCH.dnum)),
        TEST(lambda tnum, dnum: dnum > tnum // 3),
    )
    def critical_deffected(self):
        self.declare(Fact(recommendation="CRITICAL: More than 1/3 of the batch is deffected"))


    # Cracked rules
    @Rule(Cracked(cf=MATCH.cf), TEST(lambda cf: cf >= 0.8))
    def critical_cracked(self, cf):
        self.declare(
            Fact(
                recommendation="Conveyor or dough - critical cracking"
            )
        )

    @Rule(Cracked(cf=MATCH.cf), TEST(lambda cf: 0.5 <= cf < 0.8))
    def moderate_cracked(self, cf):
        self.declare(Fact(recommendation="Conveyor speed - moderate cracking"))

    @Rule(Cracked(cf=MATCH.cf), TEST(lambda cf: cf < 0.5))
    def minor_cracked(self, cf):
        self.declare(Fact(recommendation="Normal wear - minor cracking"))

    # Burned rules
    @Rule(Burned(cf=MATCH.cf), TEST(lambda cf: cf >= 0.8))
    def critical_burned(self, cf):
        self.declare(
            Fact(
                recommendation="Malfunctional Oven - critical burning"
            )
        )

    @Rule(Burned(cf=MATCH.cf), TEST(lambda cf: 0.5 <= cf < 0.8))
    def moderate_burned(self, cf):
        self.declare(
            Fact(
                recommendation="Malfunctional thermocouple or wrong settings - moderate burning"
            )
        )

    # UnderCooked rules
    @Rule(UnderCooked(cf=MATCH.cf), TEST(lambda cf: cf >= 0.8))
    def critical_undercooked(self, cf):
        self.declare(
            Fact(
                recommendation="Malfunctional Oven - critical undercook"
            )
        )

    @Rule(UnderCooked(cf=MATCH.cf), TEST(lambda cf: cf < 0.8))
    def acceptable_undercooked(self, cf):
        self.declare(
            Fact(
                recommendation="Malfunctional thermocouple or wrong settings - acceptable undercook"
            )
        )

    # Size-related rules
    @Rule(OverSized(cf=MATCH.cf), TEST(lambda cf: cf > 0.8))
    def critical_oversized(self, cf):
        self.declare(
            Fact(
                recommendation="Mold cutter deformed critical"
            )
        )

    @Rule(OverSized(cf=MATCH.cf), TEST(lambda cf: 0.5 <= cf <= 0.8))
    def moderate_oversized(self, cf):
        self.declare(
            Fact(
                recommendation="Mold cutter deformed slightly"
            )
        )

    @Rule(UnderSized(cf=MATCH.cf), TEST(lambda cf: 0.5 <= cf <= 0.8))
    def moderate_undersized(self, cf):
        self.declare(
            Fact(
                recommendation="Mold cutter deformed slightly"
            )
        )

    @Rule(UnderSized(cf=MATCH.cf), TEST(lambda cf: cf < 0.5))
    def critical_undersized(self, cf):
        self.declare(
            Fact(
                recommendation="Mold cutter deformed slightly"
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

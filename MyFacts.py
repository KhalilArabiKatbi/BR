from experta import Fact, Field


class Question(Fact):
    pass


class Answer(Fact):
    pass


class Cracked(Fact):
    cf = Field(float, mandatory=True)


class Burned(Fact):
    cf = Field(float, mandatory=True)


class UnderCooked(Fact):
    cf = Field(float, mandatory=True)


class OverSized(Fact):
    cf = Field(float, mandatory=True)


class UnderSized(Fact):
    cf = Field(float, mandatory=True)


class Contaminated(Fact):
    pass


class Prediction(Fact):
    text = Field(str, mandatory=True)
    cf = Field(float, default=100.0)


class Recommendation(Fact):
    text = Field(str, mandatory=True)

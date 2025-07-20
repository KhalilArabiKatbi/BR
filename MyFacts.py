from experta import Fact, Field


class Question(Fact):
    pass


class Answer(Fact):
    pass


class Cracked(Fact):
    percentage = Field(float, mandatory=True)
    cf = Field(float, mandatory=True)


class Burned(Fact):
    percentage = Field(float, mandatory=True)
    cf = Field(float, mandatory=True)


class UnderCooked(Fact):
    percentage = Field(float, mandatory=True)
    cf = Field(float, mandatory=True)


class OverSized(Fact):
    percentage = Field(float, mandatory=True)
    cf = Field(float, mandatory=True)


class UnderSized(Fact):
    percentage = Field(float, mandatory=True)
    cf = Field(float, mandatory=True)


class Contaminated(Fact):
    percentage = Field(float, mandatory=True)
    cf = Field(float, mandatory=True)


class Prediction(Fact):
    text = Field(str, mandatory=True)
    cf = Field(float, default=100.0)


class Recommendation(Fact):
    text = Field(str, mandatory=True)
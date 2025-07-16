from RecommendationEngine import RecommendationEngine
from MyFacts import *


class Main:
    def __init__(self):
        pass

    def main(self):
        # Sample input - keys must match exactly with lowercase
        quality_report = {
            "cracked": {"size": 18.7},
            "burned": {"percentage": 4.3},
            "over_sized": {"size": 12.0},
            "contaminated": {},
        }

        #     recommendations = self.analyze_quality(quality_report)

        #     print("Quality Control Recommendations:")
        #     for i, rec in enumerate(recommendations, 1):
        #         print(f"{i}. {rec}")

        # def analyze_quality(self, quality_data):
        #     engine = RecommendationEngine()
        #     engine.reset()

        #     # Map must use lowercase keys matching quality_report
        #     fact_classes = {
        #         "cracked": Cracked,
        #         "burned": Burned,
        #         "under_cooked": UnderCooked,
        #         "over_sized": OverSized,
        #         "under_sized": UnderSized,
        #         "contaminated": Contaminated,
        #     }

        #     for fact_name, params in quality_data.items():
        #         if fact_name in fact_classes:
        #             engine.declare(fact_classes[fact_name](**params))

        #     engine.run()
        #     return engine.recommendations

        engine = RecommendationEngine()
        engine.reset()
        engine.run()
        for fact in engine.facts.values():
            if fact.get(
                "recommendation"
            ):  # This checks for both existence and non-empty/None
                print(dict(fact))  # Print all key-value pairs
        print(engine.facts.values())


if __name__ == "__main__":
    Main().main()

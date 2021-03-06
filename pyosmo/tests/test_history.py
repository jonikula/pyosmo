from pyosmo.algorithm.weighted import WeightedAlgorithm
from pyosmo.osmo import Osmo


def test_weighted_algorithm():
    class HistoryTest:
        steps = list()

        def __init__(self):
            pass

        @staticmethod
        def weight_first():
            return 1

        def step_first(self):
            self.steps.append('step_first')

        @staticmethod
        def weight_second():
            return 2

        def step_second(self):
            self.steps.append('step_second')

        @staticmethod
        def weight_third():
            return 4

        def step_third(self):
            self.steps.append('step_third')

    model = HistoryTest()
    osmo = Osmo(model)
    osmo.tests_in_a_suite = 1
    osmo.steps_in_a_test = 1000
    osmo.algorithm = WeightedAlgorithm()
    osmo.generate()

    step_first_count = osmo.history.get_usage_count_of_test("step_first")
    step_second_count = osmo.history.get_usage_count_of_test("step_second")
    step_third_count = osmo.history.get_usage_count_of_test("step_third")

    compare_first = step_first_count * (1.0 / model.weight_first())
    compare_second = step_second_count * (1.0 / model.weight_second())
    compare_third = step_third_count * (1.0 / model.weight_third())

    assert abs(compare_first - compare_second) < 2
    assert abs(compare_first - compare_third) < 2

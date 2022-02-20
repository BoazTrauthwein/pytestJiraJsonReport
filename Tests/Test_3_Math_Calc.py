
import pytest
import sys
sys.path.append('C:\\Calc')
import calc
from datetime import datetime

# class TestCalc(OneSimInitTestCase):
project = "ASIM"
description = "Automation Demo"
test_plan_key = "ASIM-2210"
test_environment = []
test_key = "ASIM-1655"
comment = "Some comment for TestCalc class."
pytest_markers = True

class TestCalc():

    @pytest.mark.parametrize('calculation, expected', [(calc.add(10, 5), 15), (calc.add(-1, 1), 0), (calc.add(-2, -1), -3), (calc.add(0, 0), 0), (calc.add(0, 1), 1)])
    def test_step_add(self, calculation, expected):
        assert calculation == expected, "Resault of adding two numbers is {} but expected {}".format(calculation, expected) 

    @pytest.mark.parametrize('num_1, num_2, expected', [(10, 5, 5), (-1, 1, -2), (-1, 1, -2), (1, 0, 1), (1, 1, 0)])
    def test_step_subtract(self, num_1, num_2, expected):
        assert calc.subtract(num_1, num_2) == expected, "Resault of subtracting two numbers is {} but expected {}".format(num_1 - num_2, expected) 

    # def test_step_multiply(self):
    #     self.action = """Multiplyes between two numbers."""
    #     self.expected = """Multiplication"""
    #     assert calc.multiply(1, 5) == 5, "failed to multiply 10 * 5"
    #     assert calc.multiply(-2, 1) == -1, "failed to multiply -1 * 1"
    #     assert calc.multiply(-1, -1) == 1, "failed to multiply -1 * (-1)"

    # def test_step_divide(self):
    #     self.action = """Divide between two numbers."""
    #     self.expected = """Division"""
    #     assert calc.divide(1, 5) == 2, "failed to divide 10 / 5"
    #     assert calc.divide(-1, 1) == -1, "failed to divide -1 / 1"
    #     assert calc.divide(-1, -1) == 1, "failed to divide -1 / (-1)"



# if __name__ == '__main__':
#     pytest.main()
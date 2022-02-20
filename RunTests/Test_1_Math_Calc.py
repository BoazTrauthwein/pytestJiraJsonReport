
# import pytest
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
pytest_markers = False

class TestCalc():

    def test_step_add(self):
        assert calc.add(10, 5) ==  15, "failed to add 10 + 5"
        assert calc.add(-1, 1) == 0, "failed to add -1 + 1"
        assert calc.add(-1, -1) == -2, "failed to add -1 + (-1)"

    def test_step_subtract(self):
        assert calc.subtract(10, 5) == 5, "failed to subtract 10 - 5"
        assert calc.subtract(-1, 1) == -2, "failed to subtract -1 - 1"
        assert calc.subtract(-1, -1) == 0, "failed to subtract -1 - (-1)"

    def test_step_multiply(self):
        assert calc.multiply(1, 5) == 5, "failed to multiply 10 * 5"
        assert calc.multiply(-1, 1) == -1, "failed to multiply -1 * 1"
        assert calc.multiply(-1, -1) == 1, "failed to multiply -1 * (-1)"

    def test_step_divide(self):
        assert calc.divide(10, 5) == 2, "failed to divide 10 / 5"
        assert calc.divide(-1, 1) == -1, "failed to divide -1 / 1"
        assert calc.divide(-1, -1) == 1, "failed to divide -1 / (-1)"



# if __name__ == '__main__':
#     pytest.main()
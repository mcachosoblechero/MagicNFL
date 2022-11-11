import pytest
import sys

sys.path.insert(0, "c:\\Users\\Bryce Turner\\Documents\\GitHub\\MagicNFL\\src\\main")
from football_field_utils import *

def test_find_center_of_square_containing():
    assert find_center_of_square_containing((1,1), 1) == (1.5, 1.5)
    assert find_center_of_square_containing((2.1,1), 1) == (2.5, 1.5)

    assert find_center_of_square_containing((1,1), 0.5) == (1.25, 1.25)
    assert find_center_of_square_containing((105.65,8.56), 1) == (105.5, 8.5)
    assert find_center_of_square_containing((105.65,8.86), 0.25) == (105.625,8.875)
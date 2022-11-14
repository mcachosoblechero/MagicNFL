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


    #assert find_center_of_square_containing((1,1), 0.25) ==(1.125, 1.125)
    assert find_center_of_square_containing((1,1), 0.005) ==(1.0025, 1.0025)
    assert find_center_of_square_containing((1,1), 0.0005) ==(1.00025, 1.00025)
    assert find_center_of_square_containing((1,1), 0.00005) ==(1.000025, 1.000025)
    #assert find_center_of_square_containing((1,1), 0.000005) ==(1.0000025, 1.0000025)
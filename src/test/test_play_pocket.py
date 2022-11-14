import numpy as np
import pandas as pd
import sys
import math
import os
import pytest

sys.path.insert(0, "/Users/bryceturner/Personal_Projects/MagicNFL/src/main")
from field_square import *
from football_field import *
from football_field_utils import *
from play_pocket import *



left_pocket=play_pocket((30, 17.76), 1, "left", 2021090900, 97)
right_pocket=play_pocket((90, 15), 0.5, "right", 2021090901, 147)

def test_init_assignments():
    assert left_pocket.football_starting_coordinates==(30, 17.76)
    assert right_pocket.football_starting_coordinates==(90, 15)

    assert left_pocket.side_length==1
    assert right_pocket.side_length==0.5

    assert left_pocket.offenseDirection=="left"
    assert right_pocket.offenseDirection=="right"




left_pocket.set_pocket_limits(10, 7)
right_pocket.set_pocket_limits(7.3, 4.2)

def test_limit_assignments():
    assert left_pocket.xlims==(30, 40)
    assert left_pocket.ylims==(14.26, 21.26)

    assert right_pocket.xlims==(82.5, 90)
    assert right_pocket.ylims==(12.75, 17.25)



left_pocket.set_field_squares()
right_pocket.set_field_squares()

def test_pocket_field_squares():
    assert type(left_pocket.field_squares[0]) is field_square
    assert type(right_pocket.field_squares[19]) is field_square

    assert left_pocket.field_squares[0].side_length==left_pocket.side_length
    assert right_pocket.field_squares[15].side_length==right_pocket.side_length

    assert left_pocket.field_squares[1].center==(30.5, 15.76)
    assert right_pocket.field_squares[0].center==(82.75, 13)
    assert right_pocket.field_squares[1].center==(82.75, 13.5)
    
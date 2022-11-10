import pytest
import sys

sys.path.insert(0, "c:\\Users\\Bryce Turner\\Documents\\GitHub\\MagicNFL\\src\\main")
from field_square import field_square
from football_field import football_field

working_football_field_1yd=football_field((10, 20), (5, 25), 1)
working_football_field_half_yd=football_field((10, 20), (5, 25), 0.5)


def test_assignment():

    assert working_football_field_1yd.xlims==(10, 20)
    assert type(working_football_field_1yd.xlims) is tuple
    assert working_football_field_1yd.ylims==(5, 25)
    assert type(working_football_field_1yd.ylims) is tuple
    assert working_football_field_1yd.side_length==1
    assert type(working_football_field_1yd.side_length) is int


    assert working_football_field_half_yd.side_length==0.5
    assert type(working_football_field_half_yd.side_length) is float


def test_field_squares():
    working_football_field_1yd.set_field_squares()
    working_football_field_half_yd.set_field_squares()
    
    assert type(working_football_field_1yd.field_squares[0]) is field_square
    assert type(working_football_field_1yd.field_squares[19]) is field_square
    assert type(working_football_field_half_yd.field_squares[0]) is field_square
    assert type(working_football_field_half_yd.field_squares[50]) is field_square

    assert len(working_football_field_1yd.field_squares) == 200
    assert len(working_football_field_half_yd.field_squares) == 800


    assert working_football_field_1yd.field_squares[199].center==(19.5, 24.5)
    assert working_football_field_half_yd.field_squares[799].center==(19.75, 24.75)
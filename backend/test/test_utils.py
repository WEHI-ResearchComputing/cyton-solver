from cyton.api.support.upload import parse_file
from cyton.core.utils import flatten
from numpy.testing import assert_approx_equal

def test_flatten():
    assert list(flatten([1, [[2]], [3], 4, [5, 6], 7])) == [1, 2, 3, 4, 5, 6, 7]

def test_flatten_cells():
    assert list(flatten([
            # Time point 1
            [
                ['x0', 'x1', 'x2', 'x3', 'x4'], # Cell numbers per gen for replicate 1
                ['y0', 'y1', 'y2', 'y3', 'y4'], # Cell numbers per gen for replicate 2
                ['z0', 'z1', 'z2', 'z3', 'z4']], # Cell numbers per gen for replicate 3
            # Time point 2
            [
                ['a0', 'a1', 'a2', 'a3', 'a4'],
                ['b0', 'b1', 'b2', 'b3', 'b4']
            ]
        ])) == ['x0', 'x1', 'x2', 'x3', 'x4', 'y0', 'y1', 'y2', 'y3', 'y4', 'z0', 'z1', 'z2', 'z3', 'z4', 'a0', 'a1', 'a2', 'a3', 'a4', 'b0', 'b1', 'b2', 'b3', 'b4']

def test_n0():
    experiment_data = parse_file("test/SH1.119.xlsx").slice_condition_idx(0)
    n0 = experiment_data.calc_n0()
    assert_approx_equal(n0, 7477.092857142857, significant=6)

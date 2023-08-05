import pytest

from polf import quadratic_bezier_xy


@pytest.mark.parametrize(
    'p0x,p0y,p1x,p1y,p2x,p2y,t,result',
    (
        (0, 0, 0, 10, 10, 10, .5, [2.5, 7.5]),
        (0, 0, 0, 10, 10, 10, .25, [0.625, 4.375]),

        (0, 0, 10, 0, 10, 10, .5, [7.5, 2.5]),
        (0, 0, -10, 0, -10, -10, .25, [-4.375, -0.625]),
    )
)
def test_quadratic_bezier_xy(p0x, p0y, p1x, p1y, p2x, p2y, t, result):
    assert quadratic_bezier_xy(p0x, p0y, p1x, p1y, p2x, p2y, t) == result

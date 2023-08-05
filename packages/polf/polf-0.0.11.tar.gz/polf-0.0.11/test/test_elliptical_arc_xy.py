import pytest

from polf import elliptical_arc_xy


@pytest.mark.parametrize(
    'p0x,p0y,rx,ry,xAxisRotation,largeArc,sweep,p1x,p1y,t,result',
    (
        # point
        (3, 3,  0, 0, 0, 0, 0, 3, 3, .5, [3, 3]),
        (-3, -3,  0, 0, 0, 0, 0, -3, -3, .1, [-3, -3]),
        (1, -2,  0, 0, 0, 0, 0, 1, -2, .1, [1, -2]),

        # line
        (0, 0, 0, 0, 0, 0, 0, 10, 0, .5, [5, 0]),
        (0, 0, 0, 0, 0, 0, 0, -10, 0, .2, [-2, 0]),

        # Basic curve
        (0, 0, 5, 5, 0, 0, 0, 10, 0, .5, [5, 5]),
        (0, 0, 5, 5, 0, 0, 0, -10, 0, .5, [-5, -5]),
    )
)
def test_elliptical_arc_xy(p0x, p0y, rx, ry, xAxisRotation,
                           largeArc, sweep, p1x, p1y, t, result):
    assert elliptical_arc_xy(p0x, p0y, rx, ry, xAxisRotation,
                             largeArc, sweep, p1x, p1y, t) == result

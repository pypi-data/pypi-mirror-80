import pytest

from polf import cubic_bezier_xy


@pytest.mark.parametrize(
    'p0x,p0y,p1x,p1y,p2x,p2y,p3x,p3y,t,result',
    (
        (0, 0, 0, 10, 10, 10, 10, 0, .5, [5, 7.5]),
        (0, 0, 0, 10, 10, 10, 10, 0, .25, [1.5625, 5.625]),
        (0, 0, 0, -9, -9, -9, -9, 0, .5, [-4.5, -6.75]),
        (0, 10, 0, 0, 10, 0, 10, 10, .5, [5, 2.5]),
    )
)
def test_cubic_bezier_xy(p0x, p0y, p1x, p1y, p2x, p2y, p3x, p3y, t, result):
    assert cubic_bezier_xy(p0x, p0y, p1x, p1y, p2x, p2y, p3x, p3y, t) == result

import pytest

from polf import line_xyz


@pytest.mark.parametrize(
    'p0x,p0y,p0z,p1x,p1y,p1z,t,result',
    (
        (0, 0, 0, 10, 10, 10, .5, [5, 5, 5]),
        (0, 0, 0, -10, -10, -10, .5, [-5, -5, -5]),
        (-1, -1, 5, -9, -9, -5, .5, [-5, -5, 0]),
    )
)
def test_line_xyz(p0x, p0y, p0z, p1x, p1y, p1z, t, result):
    assert line_xyz(p0x, p0y, p0z, p1x, p1y, p1z, t) == result

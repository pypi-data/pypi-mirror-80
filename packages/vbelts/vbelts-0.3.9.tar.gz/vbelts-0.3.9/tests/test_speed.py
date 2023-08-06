from vbelts import speed as s
import pytest

def eval_peripheral(diam, rpm):
    return s.peripheral(diam, rpm)


def test_peripheral():
    assert eval_peripheral(240, 1750) == 21.99114857512855


def test_peripheral_fail():
    with pytest.raises(Exception):
        eval_peripheral('a', 100)
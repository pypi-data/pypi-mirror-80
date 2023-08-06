from vbelts import belt as b
import pytest

# HiPower Class

def eval_hipower(power, rpm):
    return b.HiPower(power, rpm).profile


def test_hipower():
    assert eval_hipower(3,500) == 'a'
    assert eval_hipower(70, 4000) == 'a'
    assert eval_hipower(9, 400) == 'b'
    assert eval_hipower(60, 870) == 'c'
    assert eval_hipower(90, 400) == 'd'


def test_hipower_fail():
    with pytest.raises(Exception):
        eval_hipower('a', 1000)
        eval_hipower(3, 'a')
        eval_hipower(-3, 500)
        eval_hipower(3, -500)
        eval_hipower(3, 5001)
        eval_hipower(501, 150)
        eval_hipower(3, 99)
        eval_hipower(0.9, 500)
        eval_hipower(1, None)
        eval_hipower(None, 150)


# SuperHC Class

def eval_superhc(power, rpm):
    return b.SuperHC(power, rpm).profile


def test_superhc():
    assert eval_superhc(4, 1160) == '3v'
    assert eval_superhc(30, 690) == '5v'
    assert eval_superhc(150, 575) == '8v'


def test_superhc_fail():
    with pytest.raises(Exception):
        eval_superhc('a', 1000)
        eval_superhc(3, 'a')
        eval_superhc(-3, 500)
        eval_superhc(3, -500)
        eval_superhc(0, 500)
        eval_superhc(3, 5001)
        eval_superhc(1001, 150)
        eval_superhc(3, 99)
        eval_superhc(0.9, 500)
from vbelts import power as p
import pytest

# EstPower

def eval_estpower(power, d_group, m_group, h_service):
    return p.EstPower(power, d_group, m_group, h_service).calc()


def test_estpower():
    # drive group 1
    assert eval_estpower(2, 1, 1, 4) == 2
    assert eval_estpower(2, 1, 1, 8) == 2.2
    assert eval_estpower(2, 1, 1, 18) == 2.4
    assert eval_estpower(2, 1, 2, 4) == 2.2
    assert eval_estpower(2, 1, 2, 8) == 2.4
    assert eval_estpower(2, 1, 2, 18) == 2.6
    assert eval_estpower(2, 1, 3, 4) == 2.4
    assert eval_estpower(2, 1, 3, 8) == 2.6
    assert eval_estpower(2, 1, 3, 18) == 2.8
    assert eval_estpower(2, 1, 4, 4) == 2.6
    assert eval_estpower(2, 1, 4, 8) == 2.8
    assert eval_estpower(2, 1, 4, 18) == 3
    # drive group 2
    assert eval_estpower(2, 2, 1, 4) == 2.2
    assert eval_estpower(2, 2, 1, 8) == 2.4
    assert eval_estpower(2, 2, 1, 18) == 2.6
    assert eval_estpower(2, 2, 2, 4) == 2.4
    assert eval_estpower(2, 2, 2, 8) == 2.6
    assert eval_estpower(2, 2, 2, 18) == 2.8
    assert eval_estpower(2, 2, 3, 4) == 2.8
    assert eval_estpower(2, 2, 3, 8) == 3
    assert eval_estpower(2, 2, 3, 18) == 3
    assert eval_estpower(2, 2, 4, 4) == 3.2
    assert eval_estpower(2, 2, 4, 8) == 3.2
    assert eval_estpower(2, 2, 4, 18) == 3.6


def test_estpower_fail():
    with pytest.raises(Exception):
        eval_estpower('a', 1, 1, 3)
        eval_estpower(0, 1, 1, 3)
        eval_estpower(1, 0, 1, 3)
        eval_estpower(1, 1, 0, 3)
        eval_estpower(1, 1, 1, 2)


# TransPower

def eval_transpower(b_model, b_profile, b_type, est_power, g_ratio, l_corr, min_diam, max_diam, rpm):
    return p.TransPower(b_model, b_profile, b_type, est_power, g_ratio, l_corr, min_diam, max_diam, rpm).belt_qty()


def test_transpower():
    assert eval_transpower('HiPower', 'a', 'A-32', 2, 130/240,850, 130, 240, 1750) == 0.5060451558976288


def test_transpower_fail():
    with pytest.raises(Exception):
        eval_transpower(1, 'a', 'A-32', 2, 120/240, 850, 130, 240, 1750)
from vbelts import pulley as p
import pytest

# Driven

def eval_driven_driving(diam, b_profile, power, rpm, gear_ratio):
    return p.Driven(diam, b_profile, power, rpm, gear_ratio).driving_pulley()


def test_driven_driving():
    assert eval_driven_driving(240, 'a', 3, 1750, 1.846) == 130.01083423618635


def eval_driven_commercial(diam, b_profile, power, rpm, gear_ratio, driving_pulley, desired_pulley_diam):
    return p.Driven(diam, b_profile, power, rpm, gear_ratio).commercial(driving_pulley, desired_pulley_diam)


def test_driven_commercial():
    assert eval_driven_commercial(245, 'a', 3, 1750, 1.846, 130, 120) == [240, 1.8461538461538463, 1750, 947.9166666666666]


# Driving

def eval_driving(diam, b_profile, power, rpm, gear_ratio):
    return p.Driving(diam, b_profile, power, rpm, gear_ratio).driven_pulley()


def test_driving():
    assert eval_driving(130, 'a', 3, 1000, 1.846) == 239.98000000000002
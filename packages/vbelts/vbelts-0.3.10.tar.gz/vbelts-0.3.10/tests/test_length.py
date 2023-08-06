from vbelts import length as l
import pytest

# PulleyBelt lc

def eval_pulleybelt_lc(min_diam, max_diam, belt_model, b_profile):
    return l.PulleyBelt(min_diam, max_diam, belt_model, b_profile).l_c()


def test_pulleybelt_lc():
    assert eval_pulleybelt_lc(120, 240, 'HiPower', 'a') == (1200, 'A-46')

# PulleyBelt cc

def eval_pulleybelt_ca(min_diam, max_diam, belt_model, b_profile):
    return l.PulleyBelt(min_diam, max_diam, belt_model, b_profile).c_c()


def test_pulleybelt_ca():
    assert eval_pulleybelt_ca(120, 240, 'HiPower', 'a') == 310.72814411208714
"""Pulley diameter utilities

Utilities for determining pulley mininimum diameter and related variables"""

from vbelts.util import _interpol, OutOfRangeError, NotValidError, ConvergenceError
from time import time

super_hc = [
    [485, 575, {0.5:0, 0.75:0, 1:3, 1.5:3, 2:3.8, 3:4.5, 5:4.5, 7.5:5.2, 10:6, 15:6.8, 20:8.2, 25:9, 30:10, 40:10, 50:11, 60:12, 75:14, 100:18, 125:20, 150:22, 200:22, 250:22, 300:27}],
    [575, 690, {0.5:0, 0.75:0, 1:2.5, 1.5:3, 2:3, 3:3.8, 5:4.5, 7.5:4.5, 10:5.2, 15:6, 20:6.8, 25:8.2, 30:9, 40:10, 50:10, 60:11, 75:13, 100:15, 125:18, 150:20, 200:22, 250:22, 300:27}],
    [690, 870, {0.5:2.2, 0.75:2.4, 1:2.4, 1.5:2.4, 2:3, 3:3, 5:3.8, 7.5:4.4, 10:4.4, 15:5.2, 20:6, 25:6.8, 30:6.8, 40:8.2, 50:8.4, 60:10, 75:9.5, 100:12, 125:15, 150:18, 200:22}],
    [870, 1160, {0.5:0, 0.75:2.2, 1:2.4, 1.5:2.4, 2:2.4, 3:3, 5:3, 7.5:3.8, 10:4.4, 15:4.4, 20:5.2, 25:6, 30:6.8, 40:6.8, 50:8.2, 60:8, 75:10, 100:10, 125:12, 150:13}],
    [1160, 1750, {0.5:0, 0.75:0, 1:2.2, 1.5:2.4, 2:2.4, 3:2.4, 5:3, 7.5:3, 10:3.8, 15:4.4, 20:4.4, 25:4.4, 30:5.2, 40:6, 50:6.8, 60:7.4, 75:8.6, 100:8.6, 125:10.5, 150:10.5, 200:13.2}],
    [1750, 3450, {0.5:0, 0.75:0, 1:0, 1.5:2.2, 2:2.4, 3:2.4, 5:2.4, 7.5:3, 10:3, 15:3.8, 20:4.4, 25:4.4}]
]

hi_power_2 = [
    [485, 575, {0.5:2.5, 0.75:3, 1:3, 1.5:3, 2:3.8, 3:4.5, 5:4.5, 7.5:5.2, 10:6, 15:6.8, 20:8.2, 25:9, 30:10, 40:10, 50:11, 60:12, 75:14, 100:18, 125:20, 150:22, 200:22, 250:22, 300:27}],
    [575, 690, {0.5:2.5, 0.75:2.5, 1:3, 1.5:3, 2:3, 3:3.8, 5:4.5, 7.5:4.5, 10:5.2, 15:6, 20:6.8, 25:8.2, 30:9, 40:10, 50:10, 60:11, 75:13, 100:15, 125:18, 150:20, 200:22, 250:22, 300:27}],
    [690, 870, {0.5:2.2, 0.75:2.4, 1:2.4, 1.5:2.4, 2:3, 3:3, 5:3.8, 7.5:4.4, 10:4.6, 15:5.4, 20:6, 25:6.8, 30:6.8, 40:8.2, 50:9.0, 60:10, 75:10.5, 100:12.5, 125:15, 150:18, 200:22}],
    [870, 1160, {0.5:0, 0.75:2.2, 1:2.4, 1.5:2.4, 2:2.4, 3:3, 5:3, 7.5:3.8, 10:4.4, 15:4.6, 20:5.4, 25:6, 30:6.8, 40:6.8, 50:8.2, 60:9, 75:10, 100:11, 125:12.5, 150:13}],
    [1160, 1750, {0.5:0, 0.75:0, 1:2.2, 1.5:2.4, 2:2.4, 3:2.4, 5:3, 7.5:3, 10:3.8, 15:4.4, 20:4.6, 25:5, 30:5.4, 40:6, 50:6.8, 60:7.4, 75:9, 100:10, 125:11.5}],
    [1750, 3450, {0.5:0, 0.75:0, 1:0, 1.5:2.2, 2:2.4, 3:2.4, 5:2.6, 7.5:3, 10:3, 15:3.8, 20:4.4, 25:4.4}]
]


def _diam(vbelt_list:list, power:float, speed:float):
    """Chooses the minimum diameter in a list containing engine power and rpm
    :param vbelt_list: list of pulley diameters containing speed range and engine power
    :type vbelt_list: list
    :param power: engine power, hp
    :type power: float
    :param speed: rotation speed of the engine, rpm
    :type speed: float
    :return: pulley diameter, in
    :rtype: float
    """
    for item in vbelt_list:
        if item[0] <= speed < item[1]:
            last_power = 0
            last_diam = 0
            for key in item[2].keys():  # loops through the keys of dict
                if power == key:
                    if item[2].get(key) == 0:  # zero diameter is not valid
                        raise OutOfRangeError('Value out of range for these parameters')
                    else:
                        return item[2].get(key)
                elif key > power:
                    power_max = key
                    diam_max = item[2].get(key)
                    power_min = last_power
                    diam_min = last_diam
                    pulley_diam = _interpol(power, power_min, power_max, diam_min, diam_max)  # interpolates using the function
                    if pulley_diam == 0:  # zero diameter is not valid
                        raise OutOfRangeError('Value out of range for these parameters')
                    return pulley_diam
                last_power = key  # stores the last power
                last_diam = item[2].get(key)  # stores the last diameter
            raise OutOfRangeError('Value out of range for these parameters')


def min_pulley(vbelt_model:str, axle_power:float, axle_speed:float, mode='si'):
    """Minimum pulley diameter given the drive power and speed
    :param vbelt_model: set the v-belt model, use `super_hc` or `hi_power`
    :type vbelt_model: str
    :param axle_power: power on the pulley axle, hp
    :type axle_power: float
    :param axle_speed: rotational speed of the fastest axle, rpm
    :type axle_speed: float
    :param mode: define the return units, defaults to `si`
    :type mode: str, optional
    :return: minimum diameter of the pulley
    :rtype: float
    """
    # chooses the model
    if vbelt_model == 'super_hc':
        li = super_hc
    elif vbelt_model == 'hi_power':
        li = hi_power_2
    else:
        raise NotValidError("Value of the vbelt_model variable is not valid")
    diameter = _diam(li, axle_power, axle_speed)
    if mode == 'si':
        return 25.4 * diameter
    elif mode == 'imp':
        return diameter
    else:
        raise ValueError


def driven_pulley(driving_pulley_diam:float, gear_ratio:float):
    """Driven pulley diameter given the driving pulley diameter
    :param driving_pulley_diam: diameter of the driving pulley, mm
    :type driving_pulley_diam: float
    :param gear_ratio: gear ratio of the pulleys in decimal form
    :type gear_ratio: float
    :return: driven pulley diameter, mm
    :rtype: float
    """
    # check for the right data type
    if isinstance(driving_pulley_diam, (float, int)) and isinstance(gear_ratio, (float, int)):
        return driving_pulley_diam * gear_ratio
    else:
        raise ValueError


def driving_pulley(driven_pulley_diam:float, gear_ratio:float):
    """Driving pulley diameter given the driven pulley diameter
    :param driven_pulley_diam: diameter of the driven pulley, mm
    :type driven_pulley_diam: float
    :param gear_ratio: gear ratio of the pulleys in decimal form
    :type gear_ratio: float
    :return: driving pulley diameter, mm
    :rtype: float
    """
    # check for the right data type
    if isinstance(driven_pulley_diam, (float, int)) and isinstance(gear_ratio, (float, int)):
        return driven_pulley_diam/gear_ratio
    else:
        raise ValueError


def driven_commercial(gear_ratio:float, rpm_input:float, driving_pulley:float, desired_pulley_diam:int):
    """Selects an approximate to the commercial diameter of a pulley through convergence
    :param gear_ratio: reference gear ratio in decimal form
    :type gear_ratio: float
    :param rpm_input: rotational speed of the driving axle, rpm
    :type rpm_input: float
    :param driving_pulley: diameter of the driving pulley, mm
    :type driving_pulley: float
    :param desired_pulley_diam: desired diameter of the driven pulley, mm
    :type desired_pulley_diam: int
    :return: a list with the calculated driven diameter, new gear ratio for this diameter, driving and driven speed of the axles
    :rtype: list
    """
    # calculate gear ratio range
    range_rpm = 100
    rpm_output = rpm_input/gear_ratio
    gear_ratio_max = rpm_input/(rpm_output - range_rpm)
    gear_ratio_min = rpm_input/(rpm_output + range_rpm)
    error_min = 0.01
    driven_pulley = gear_ratio * driving_pulley
    diam_calc = driven_pulley

    # iterate
    error = 1
    t_i = time()
    while error > error_min:
        gear_ratio_calc = diam_calc/driving_pulley
        # control iteration parameters
        if gear_ratio_calc > gear_ratio_max:
            diam_calc -= diam_calc * error * 0.01
        elif gear_ratio_calc < gear_ratio_min:
            diam_calc += diam_calc * error
        else:
            diam_calc *= error
        error = 1-(diam_calc/desired_pulley_diam)
        # control for infinite loops
        t_f = time()
        elapsed_time = t_f - t_i
        if elapsed_time > 4:
            raise ConvergenceError('The function could not reach convergence, try again with a lower value')
    
    # recalculate rpm_output
    base = 10
    diam_out = base * round(diam_calc/base)  # round the number to nearest 5 integer
    gear_ratio_out = diam_out/driving_pulley
    rpm_out = rpm_input/gear_ratio_out
    return [diam_out, gear_ratio_calc, rpm_input, rpm_out]
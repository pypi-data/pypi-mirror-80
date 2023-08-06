"""Force (REVIEW)
"""
from math import pi, exp
from vbelts.util import _read_csv_data, _Iterate, _Interpolate, _OutOfRangeError






def torque(power:float, rpm_pulley:float):
    """Torque on the pulley
    :param power: power of the system, hp
    :type power: float
    :param rpm_pulley: rotational speed of the pulley, rpm
    :type rpm_pulley: float
    :return: torque of the pulley in kgf*m
    :rtype: float
    """
    return (2250*power)/(pi*rpm_pulley)


def _contact_arc_rad(factor:float):
    """Searches and _Interpolates a factor on a csv data table
    :param factor: factor (D-d)/Ca
    :type factor: float
    :return: angle of the contact between v-belt and pulley, rad
    :rtype: float
    """
    last_factor = 0
    last_contact_arc = 180
    for line in _read_csv_data('fcac_contact_arc'):
        if line['factor'] == factor:
            contact_arc = line['contact_arc']
            return (pi*contact_arc/180)
        elif last_factor < factor < line['factor']:
            contact_arc = _interpol(factor, last_factor, line['factor'], last_contact_arc, line['contact_arc'])
            return (pi*contact_arc/180)
        last_factor = line['factor']
        last_contact_arc = line['contact_arc']
    raise _OutOfRangeError('Value out of range for these parameters')


def _fric_coef(belt_material:str='rubber', pulley_material:str='steel'):
    """Select coefficient of friction from csv data table
    :param belt_material: material of the belt, select between `polyurethane`, `nylon` and `rubber`, defaults to `rubber`
    :type belt_material: str, optional
    :param pulley_material: material of the pulley, select between `steel` and `aluminum`, defaults to `steel`
    :type pulley_material: str, optional
    :return: friction coefficient
    :rtype: float
    """
    for line in _read_csv_data('fric_coef'):
        if line['belt_material'] == belt_material:
            if line['pulley_material'] == pulley_material:
                return line['fric_coef']
    raise _OutOfRangeError('Value out of range for these parameters')


def _forces(m_torque:float, diam_driving:float, diam_driven:float, corr_distance_pulleys:float, belt_material:str='rubber', pulley_material:str='steel'):
    """Main forces of the pulley/belt system
    :param m_torque: torque of the system, kgf*m
    :type m_torque: float
    :param diam_driving: diameter of the driving pulley, mm
    :type diam_driving: float
    :param diam_driven: diameter of the driven pulley, mm
    :type diam_driven: float
    :param corr_distance_pulleys: corrected distance between the pulley's center, mm
    :type corr_distance_pulleys: float
    :param belt_material: material of the belt, select between `polyurethane`, `nylon` and `rubber`, defaults to `rubber`
    :type belt_material: str, optional
    :param pulley_material: material of the pulley, select between `steel` and `aluminum`, defaults to `steel`
    :type pulley_material: str, optional
    :return: list of three main force values, f_0, f_1 and f_z, all in kgf
    :rtype: list
    """
    f_u = (m_torque * 9.81)/(diam_driving/(2 * 1000))
    factor_contact = (max(diam_driving, diam_driven) - min(diam_driving, diam_driven))/corr_distance_pulleys
    carc_rad = _contact_arc_rad(factor_contact)
    mu = _fric_coef(belt_material, pulley_material)    
    f_0 = (f_u/(exp(mu*carc_rad)-1))/9.81
    f_1 = (f_u*(exp(mu*carc_rad)/(exp(mu * carc_rad)-1)))/9.81
    f_z = (f_u*(exp(mu*carc_rad)+1)/(exp(mu * carc_rad)-1))/9.81
    return [f_0, f_1, f_z]


def axle(m_torque:float, diam_driving:float, diam_driven:float, corr_distance_pulleys:float, belt_material:str='rubber', pulley_material:str='steel'):
    """Axle force on the pulley
    :param m_torque: torque of the system, kgf*m
    :type m_torque: float
    :param diam_driving: diameter of the driving pulley, mm
    :type diam_driving: float
    :param diam_driven: diameter of the driven pulley, mm
    :type diam_driven: float
    :param corr_distance_pulleys: corrected distance between the pulley's center, mm
    :type corr_distance_pulleys: float
    :param belt_material: material of the belt, select between `polyurethane`, `nylon` and `rubber`, defaults to `rubber`
    :type belt_material: str, optional
    :param pulley_material: material of the pulley, select between `steel` and `aluminum`, defaults to `steel`
    :type pulley_material: str, optional
    :return: axle force on the pulley, kgf
    :rtype: float
    """
    return (_forces(m_torque, diam_driving, diam_driven, corr_distance_pulleys, belt_material, pulley_material)[2])


def tangential(m_torque:float, diam_driving:float, diam_driven:float, corr_distance_pulleys:float, belt_material:str='rubber', pulley_material:str='steel'):
    """Tangential force on the v-belt
    :param m_torque: torque of the system, kgf*m
    :type m_torque: float
    :param diam_driving: diameter of the driving pulley, mm
    :type diam_driving: float
    :param diam_driven: diameter of the driven pulley, mm
    :type diam_driven: float
    :param corr_distance_pulleys: corrected distance between the pulley's center, mm
    :type corr_distance_pulleys: float
    :param belt_material: material of the belt, select between `polyurethane`, `nylon` and `rubber`, defaults to `rubber`
    :type belt_material: str, optional
    :param pulley_material: material of the pulley, select between `steel` and `aluminum`, defaults to `steel`
    :type pulley_material: str, optional
    :return: tangential force on the pulley, kgf
    :rtype: float
    """
    ft_1, ft_2 = _forces(m_torque, diam_driving, diam_driven, corr_distance_pulleys, belt_material, pulley_material)[:2]
    return (ft_1 - ft_2)
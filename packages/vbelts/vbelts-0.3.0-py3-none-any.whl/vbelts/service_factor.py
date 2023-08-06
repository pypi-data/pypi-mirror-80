"""Service Factor

This module calculate the service factor for v-belts."""

import re

mach_group_data = [
    ['stirrer', '1'],
    ['small blower', '1'],
    ['exhaustor', '1'],
    ['centrifugal pump', '1'],
    ['regular compressor', '1'],
    ['light conveyor belt', '1'],
    ['heavy conveyor belt', '2'],
    ['large blower', '2'],
    ['generator', '2'],
    ['transmission axle', '2'],
    ['laundry machine', '2'],
    ['press', '2'],
    ['graphical machine', '2'],
    ['positive displacement pump', '2'],
    ['sieving machine', '2'],
    ['pottery machine', '3'],
    ['bucket elevator', '3'],
    ['reciprocating compressor', '3'],
    ['mill', '3'],
    ['carpentry machine', '3'],
    ['textile machine', '3'],
    ['crusher', '4'],
    ['crane', '4'],
    ['tire shop machine', '4'],
]

drive_group_data = [
    ['normal torque ac', '1'],
    ['ring cage ac', '1'],
    ['synchronous ac', '1'],
    ['phase division ac', '1'],
    ['derivation dc', '1'],
    ['multiple cylinder combustion', '1'],
    ['high torque ac', '2'],
    ['high slipping ac', '2'],
    ['repulsion induction ac', '2'],
    ['monophasic ac', '2'],
    ['series winding dc', '2'],
    ['collector rings ac', '2'],
    ['mixed winding dc', '2'],
    ['single cylinder combustion', '2'],
    ['transmission axle', '2'],
    ['clutch', '2'],
]


def _group(entry, comp_list):
    """Searches the comp_list for the string in the entry and returns the second item
    :param entry: string for the search
    :type entry: str
    :param comp_list: list of lists that contains the values used on the search
    :type comp_list: list
    :return: second item on the sublist that matches the string
    :rtype: int
    """
    data_regex = re.compile(entry)
    try:
        for item in comp_list:
            m = data_regex.search(item[0])  # search the first item
            if m is not None:
                return int(item[1])
    except:  # stop the execution if nothing is found
        raise ValueError

def _sf_partial(mach_group, service_hours):
    """Select the partial result for the service factor
    :param mach_group: machine group for the searched entry
    :type mach_group: int
    :param service_hours: hours of service per day of the machine
    :type service_hours: float
    :return: partial service factor
    :rtype: float
    """
    if mach_group == 1:
        if 0 < service_hours <= 5:
            sf_part = 1.0
        elif 5 < service_hours <= 10:
            sf_part = 1.1
        elif 10 < service_hours <= 24:
            sf_part = 1.2
    elif mach_group == 2:
        if 0 < service_hours <= 5:
            sf_part = 1.1
        elif 5 < service_hours <= 10:
            sf_part = 1.2
        elif 10 < service_hours <= 24:
            sf_part = 1.3
    elif mach_group == 3:
        if 0 < service_hours <= 5:
            sf_part = 1.2
        elif 5 < service_hours <= 10:
            sf_part = 1.3
        elif 10 < service_hours <= 24:
            sf_part = 1.4
    elif mach_group == 4:
        if 0 < service_hours <= 5:
            sf_part = 1.3
        elif 5 < service_hours <= 10:
            sf_part = 1.4
        elif 10 < service_hours <= 24:
            sf_part = 1.5
    return sf_part

def _calc(mach_group, drive_group, _sf_p):
    """Select and calculate the main service factor
    :param mach_group: machine group for a data entry
    :type mach_group: int
    :param drive_group: drive group for a data entry
    :type drive_group: int
    :param _sf_p: partial service factor
    :type _sf_p: float
    :return: service factor
    :rtype: float
    """
    if mach_group == 1 and drive_group == 2:
        result = _sf_p + 0.1
    elif mach_group == 2 and drive_group == 2:
        result = _sf_p + 0.1
    elif mach_group == 3 and drive_group == 2:
        if _sf_p == 1.4:
            result = _sf_p + 0.1
        else:
            result = _sf_p + 0.2
    elif mach_group == 4 and drive_group == 2:
        if _sf_p == 1.4:
            result = _sf_p + 0.2
        else:
            result = _sf_p + 0.3
    else:
        result = _sf_p
    return round(result, 1)

        
def service_factor(machine:str, drive:str, hours_service:float, mach_list=mach_group_data, drive_list=drive_group_data):
    """Calculate the service factor based on the machine driven, the drive and hours of service per day
    :param machine: type of machine driven, for valid values see the documentation
    :type machine: str
    :param drive: type of drive for the machine, for valid values see the documentation
    :type drive: str
    :param hours_service: hours of service of the system
    :type hours_service: float
    :param mach_list: valid machine list, defaults to mach_group_data
    :type mach_list: variable, optional
    :param drive_list: valid drive list, defaults to drive_group_data
    :type drive_list: variable, optional
    :return: service factor
    :rtype: float
    """
    machine_group = _group(machine, mach_list)
    drive_group = _group(drive, drive_list)
    precalc = _sf_partial(machine_group, hours_service)
    result = _calc(machine_group, drive_group, precalc)
    return result

"""
Utilities
=========

"""

import csv
import os
import re
from abc import ABC, abstractmethod

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
    ['multiple cylinders combustion', '1'],
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

class _OutOfRangeError(Exception):
    """Raised when value is out of range of the list"""
    pass

class _NotValidError(Exception):
    """Raised when the value passed to the function is not valid"""
    pass


class _ConvergenceError(Exception):
    """Raised when the value passed to an iterator function does not converge"""
    pass


class _Interpolate():
    """Interpolate class linear interpolate values.
    
    Parameters
    ----------
    x_data : float
        Input data point to be calculated, [-]
    x_min : float
        Nearest minimum input value in relation to the data point, [-]
    x_max : float
        Nearest maximum input value in relation to the data point, [-]
    y_min : float
        Nearest minimum output value in relation to the data point, [-]
    y_max : float
        Nearest maximum output value in relation to the data point, [-]
    """
    def __init__(self, x_data, x_min, x_max, y_min, y_max):
        self.x_data = x_data
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
    
    def y_data(self):
        """Linear interpolation of table data

        Returns
        -------
        x : float
            Interpolated output data point
        """
        return self.y_max-((self.x_max - self.x_data)/(self.x_max - self.x_min))*(self.y_max - self.y_min)


class _MinDist():
    """MinDist class selects the nearest data value from a point in between.

    Parameters
    ----------
    x : float
        Value on the interval, [-]
    x_min : float
        Nearest minimum value on the scale, [-]
    x_max : float
        Nearest maximum value on the scale, [-]
    """
    def __init__(self, x:float, x_min:float, x_max:float):
        self.x = x
        self.x_min = x_min
        self.x_max = x_max
    
    def calc(self):
        """Nearest value between two items given one value that is in the interval.

        Returns
        -------
        x_nearest : float
            Nearest value of x
        """
        dist_1 = (self.x - self.x_min)/self.x
        dist_2 = (self.x_max - self.x)/self.x
        if dist_1 < dist_2:
            return self.x_min
        elif dist_1 > dist_2:
            return self.x_max
        elif dist_1 == dist_2: # if both are equal, return the maximum
            return self.x_max
        else:
            raise ValueError


class _CSV(ABC):
    """Abstract class for handling csv files"""
    @abstractmethod
    def read(self): pass


class _Iterate(_CSV):
    """Iterate class is responsible for iterating through the multiple csv files in the package.
    
    Parameters
    ----------
    filename : str
        Filename of the csv file without the extension, [-]
    row : str
        Rows of data of the csv file, [-]
    """
    def __init__(self, filename:str, *row:str, interpol:_Interpolate=_Interpolate, m_dist:_MinDist=_MinDist):
        self.filename = filename
        self.row = row
        self.interpol = interpol
        self.m_dist = m_dist

    def read(self):
        """Read csv data and return a generator function.
        
        Returns
        -------
        x : generator
            Generator data, [-]
        """
        file_path = os.path.join(os.path.dirname(__file__), 'data', self.filename)  # fetch full path
        with open(f'{file_path}.csv', mode='r', encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file, quoting=csv.QUOTE_NONNUMERIC)  # not quoted values are floats
            # next(reader)
            for line in reader:
                yield line
    

    def fcc(self, vbelt_model:str, vbelt_type:str):
        self.filename = f'{vbelt_model}_fcc'
        for line in self.read():
            if line['type'] == vbelt_type:
                return float(line['fcc'])

    
    def three_rows(self, *param:float):
        """_Iterate through a file with a list of three rows using two parameters and return the last one, _Interpolated or not
        """
        for line in self.read():
            if line[self.row[0]] == param[0]:
                if line[self.row[1]] == param[1]:
                    return (line[self.row[2]], False)  # first return the value, second need for adjusting, used in TransPower._basic()
                elif line[self.row[1]] > param[1]:
                    return (self.interpol(param[1], last_row_1, line[self.row[1]], last_row_2, line[self.row[2]]).y_data(), False)
            elif line[self.row[0]] > param[0]:
                if line[self.row[1]] == param[1]:
                    return (self.interpol(param[1], last_row_1, line[self.row[1]], last_row_2, line[self.row[2]]).y_data(), True)
                elif line[self.row[1]] > param[1]:
                    return (self.interpol(), True)
            last_row_1 = line[self.row[1]]
            last_row_2 = line[self.row[2]]
        raise _OutOfRangeError('Value out of range for these parameters')


    def three_rows_choose(self, param, w_row:float):
        """_Iterate through a file with a list of three rows using one parameter, chosing which row to use to return the value.
        """
        w_row -= 1
        last_row_1 = 0
        last_row_chosed = 0
        for line in self.read():
            if line[self.row[0]] == param:
                return line[self.row[w_row]]
            elif line[self.row[0]] > param:
                return self.interpol(param, last_row_1, line[self.row[0]], last_row_chosed, line[self.row[w_row]]).y_data()
            last_row_1 = line[self.row[0]]
            last_row_chosed = line[self.row[w_row]]
        raise _OutOfRangeError('Value out of range for these parameters')


    def four_rows(self, *param:float):
        """_Iterate through a file with a list of four rows using two parameters, the first two are a range, and return the last, _Interpolated or not.
        """
        for line in self.read():
            if line[self.row[0]] > param[0]:
                raise _OutOfRangeError('Value out of range for these parameters')
            elif line[self.row[0]] <= param[0] < line[self.row[1]]:
                if line[self.row[2]] == param[1]:
                    return line[self.row[3]]
                elif line[self.row[2]] > param[1]:
                    return self.interpol(param[1], last_row_2, line[self.row[2]], last_row_3, line[self.row[3]]).y_data()
            last_row_2 = line[self.row[2]]
            last_row_3 = line[self.row[3]]
        raise _OutOfRangeError('Value out of range for these parameters')

    
    def belt_type(self, *param:float):
        for line in self.read():
            if line[self.row[0]] == param[0]:
                last_length = 0
                if line[self.row[1]] == param[1]:  # if length == length on data
                    return (line[self.row[1]], line[self.row[2]])
                elif line[self.row[1]] > param[1]:
                    chosed_length = self.m_dist(param[1], last_length, line[self.row[1]]).calc()
                    # check what length and type was chosen and return them
                    if chosed_length == line[self.row[1]]:
                        chosed_type = line[self.row[2]]
                    else:
                        chosed_type = last_type
                    return (chosed_length, chosed_type)
            last_length = line[self.row[1]]
            last_type = line[self.row[2]]
        raise _OutOfRangeError('Value out of range for these')


class _Device():
    r"""Device class creates the blueprint for the Motor and Machine classes.

    Parameters
    ----------
    name : str
        Device name, [-]
    li_group : list
        Device group list, [-]

    Attributes
    ----------
    group : int
        Device group classification, [-]
    """
    def __init__(self, name:str, li_group:list):
        self.name = name
        self.li_group = li_group
        self.group = self._grp()
    

    def _grp(self):
        r"""Classifies the device group based on the name using the self.li_group.

        Returns
        -------
        group : int
            Device group
        """
        data_regex = re.compile(r'(\w+).?(\w+)?.?(\w+)?')
        try:
            for item in self.li_group:
                m = data_regex.search(item[0])  # search the first item
                if self.name in m.group(0):
                    return int(item[1])
        except:  # stop the execution if nothing is found
            raise ValueError


class Motor(_Device):
    r"""Motor class centralizes and classifies engine properties. For valid motor data entries see the :ref:`Data <motor_machine_data>` section.

    Parameters
    ----------
    name : str
        Motor name, [-]
    power : float
        Motor power, [hp]

    Attributes
    ----------
    group : int
        Motor group classification, [-]
    
    Examples
    --------
    >>> engine = vbelts.util.Motor('multiple cylinders', 3)
    >>> engine.group
    1
    >>> engine.power
    3
    
    Notes
    -----
    The group classification is needed for the service factor [#]_ calculation.

    References
    ----------
    .. [#] Oleostatic. 2016. "OLEOSTATIC Correas Trapeciales Convencionales", **Universidad Carlos III de Madrid**. Accessed September 23, 2020. http://ocw.uc3m.es/ingenieria-mecanica/diseno-mecanico-1/material_clase/ocw_catalogo_correas.
    """
    def __init__(self, name:str, power:float):
        super().__init__(name, li_group=drive_group_data)
        self.power = power
        self.li_group = drive_group_data


class Machine(_Device):
    r"""Machine class centralizes and classifies engine properties. For valid machine data entries see the :ref:`Data <motor_machine_data>` section.

    Parameters
    ----------
    name : str
        Machine name, [-]
    hours_service : float
        Hours of service per day, [h/day]

    Attributes
    ----------
    group : int
        Machine group classification, [-]
    
    Examples
    --------
    >>> mach = vbelts.util.Machine('reciprocating compressor', 18)
    >>> mach.group
    3
    >>> mach.hours_service
    18
    
    Notes
    -----
    The group classification is needed for the service factor [#]_ calculation.

    References
    ----------
    .. [#] Oleostatic. 2016. "OLEOSTATIC Correas Trapeciales Convencionales", **Universidad Carlos III de Madrid**. Accessed September 23, 2020. http://ocw.uc3m.es/ingenieria-mecanica/diseno-mecanico-1/material_clase/ocw_catalogo_correas.
    """
    def __init__(self, name:str, hours_service:float):
        super().__init__(name, li_group=mach_group_data)
        self.hours_service = hours_service
        self.li_group = mach_group_data


class _Belt():
    """Belt is a blueprint class for the HiPower and SuperHC v-belt classes"""
    def __init__(self, est_power:float, rpm_fastest:float):
        self.est_power = est_power
        self.rpm_fastest = rpm_fastest


    def _fun_val(self, a:float, b:float, c:float, x:float, upper:float):
        """X for a mathematical function with a linear (ax + b) and a constant part.


        :param a: a coefficient for the linear part of the function
        :type a: float
        :param b: b coefficient for the linear part of the function
        :type b: float
        :param c: y value for the constant part of the function
        :type c: float
        :param x: input value of x
        :type x: float
        :param upper: upper limit of the linear function in the y axis
        :type upper: float
        :return: y value for the math function
        :rtype: float
        """
        if x < upper:
            eq = a * x + b
            return abs(eq)
        # if the value is within the constant range
        elif x >= upper:
            eq = c
            return eq


class _Pulley(ABC):
    """Abstract class for the Driven and Driving pulley class"""
    def __init__(self, diam, vbelt_profile:str, power:float, rpm:float, iterator:_Iterate=_Iterate):
        self.diam = diam
        self.vbelt_profile = vbelt_profile
        self.power = power
        self.rpm = rpm
        self.filename = f'{self.vbelt_profile}_diam'
        self.iterator = iterator

    # @abstractmethod
    # def min_diam(self): pass


def gear_ratio(rpm_input:float, rpm_output:float):
    r"""Pulley gear ratio based on the rpm input and output.

    Parameters
    ----------
    rpm_input : float
        input (driving) axle speed, [rpm]
    rpm_output : float
        output (driven) axle speed, [rpm]
    
    Returns
    -------
    gear_ratio : float
        Calculated gear ratio, [-]
    
    Examples
    --------
    >>> vbelts.util.gear_ratio(1000, 1750)
    0.5714285714285714
    
    Notes
    -----
    The rpm based gear ratio is calculated [#]_ as:

    .. math::
        R = \frac{N_{in}}{N_{out}}
    
    References
    ----------
    .. [#] Douglas Wright. 2005."DANotes: V-Belt drives: Introduction", **V-BELT DRIVES**. Accessed September 23, 2020, http://www-mdp.eng.cam.ac.uk/web/library/enginfo/textbooks_dvd_only/DAN/V-belts/intro/intro.html.
    """
    if isinstance(rpm_input, (float, int)) and isinstance(rpm_output, (float, int)):
        return rpm_input/rpm_output
    else:
        raise ValueError

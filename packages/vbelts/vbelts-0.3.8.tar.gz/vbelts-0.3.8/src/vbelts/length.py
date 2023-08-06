from vbelts.util import _Interpolate, _Iterate, _ReIterate, _OutOfRangeError
from abc import ABC

h_factor = {0:0, 0.02:0.01, 0.04:0.02, 0.06:0.03, 0.08:0.04, 0.1:0.05, 0.12:0.06, 0.14:0.07, 0.16:0.08, 0.18:0.09, 0.2:0.1, 0.21:0.11, 0.23:0.12, 0.25:0.13, 0.27:0.14, 0.29:0.15, 0.3:0.16, 0.32:0.17, 0.34:0.18, 0.35:0.19, 0.37:0.2, 0.39:0.21, 0.4:0.22, 0.41:0.23, 0.43:0.24, 0.44:0.25, 0.46:0.26, 0.47:0.27, 0.48:0.28, 0.5:0.29, 0.51:0.3}
HiPower_length = ({'profile': 'a', 'length': '695', 'type': 'A-26'}, {'profile': 'a', 'length': '720', 'type': 'A-27'}, {'profile': 'a', 'length': '820', 'type': 'A-31'}, {'profile': 'a', 'length': '845', 'type': 'A-32'}, {'profile': 'a', 'length': '870', 'type': 'A-33'}, {'profile': 'a', 'length': '920', 'type': 'A-35'}, {'profile': 'a', 'length': '975', 'type': 'A-37'}, {'profile': 'a', 'length': '1000', 'type': 'A-38'}, {'profile': 'a', 'length': '1075', 'type': 'A-41'}, {'profile': 'a', 'length': '1100', 'type': 'A-42'}, {'profile': 'a', 'length': '1175', 'type': 'A-45'}, {'profile': 'a', 'length': '1200', 'type': 'A-46'}, {'profile': 'a', 'length': '1225', 'type': 'A-47'}, {'profile': 'a', 'length': '1280', 'type': 'A-49'}, {'profile': 'a', 'length': '1305', 'type': 'A-50'}, {'profile': 'a', 'length': '1330', 'type': 'A-51'}, {'profile': 'a', 'length': '1380', 'type': 'A-53'}, {'profile': 'a', 'length': '1405', 'type': 'A-54'}, {'profile': 'a', 'length': '1430', 'type': 'A-55'}, {'profile': 'a', 'length': '1480', 'type': 'A-57'}, {'profile': 'a', 'length': '1555', 'type': 'A-60'}, {'profile': 'a', 'length': '1610', 'type': 'A-62'}, {'profile': 'a', 'length': '1660', 'type': 'A-64'}, {'profile': 'a', 'length': '1710', 'type': 'A-66'}, {'profile': 'a', 'length': '1760', 'type': 'A-68'}, {'profile': 'a', 'length': '1785', 'type': 'A-69'}, {'profile': 'a', 'length': '1835', 'type': 'A-71'}, {'profile': 'a', 'length': '1940', 'type': 'A-75'}, {'profile': 'a', 'length': '2065', 'type': 'A-80'}, {'profile': 'a', 'length': '2190', 'type': 'A-85'}, {'profile': 'a', 'length': '2320', 'type': 'A-90'}, {'profile': 'a', 'length': '2470', 'type': 'A-96'}, {'profile': 'a', 'length': '2700', 'type': 'A-105'}, {'profile': 'a', 'length': '2880', 'type': 'A-112'}, {'profile': 'a', 'length': '3080', 'type': 'A-120'}, {'profile': 'a', 'length': '3285', 'type': 'A-128'}, {'profile': 'a', 'length': '3485', 'type': 'A-136'}, {'profile': 'a', 'length': '3690', 'type': 'A-144'}, {'profile': 'a', 'length': '4045', 'type': 'A-158'}, {'profile': 'a', 'length': '4150', 'type': 'A-162'}, {'profile': 'a', 'length': '4425', 'type': 'A-173'}, {'profile': 'a', 'length': '4605', 'type': 'A-180'}, {'profile': 'b', 'length': '935"', 'type': 'B-35'}, {'profile': 'b', 'length': '985"', 'type': 'B-37'}, {'profile': 'b', 'length': '1010"', 'type': 'B-38'}, {'profile': 'b', 'length': '1035"', 'type': 'B-39'}, {'profile': 'b', 'length': '1115', 'type': 'B-42'}, {'profile': 'b', 'length': '1215', 'type': 'B-46'}, {'profile': 'b', 'length': '1265', 'type': 'B-48'}, {'profile': 'b', 'length': '1315', 'type': 'B-50'}, {'profile': 'b', 'length': '1340', 'type': 'B-51'}, {'profile': 'b', 'length': '1365', 'type': 'B-52'}, {'profile': 'b', 'length': '1390', 'type': 'B-53'}, {'profile': 'b', 'length': '1445', 'type': 'B-55'}, {'profile': 'b', 'length': '1570', 'type': 'B-60'}, {'profile': 'b', 'length': '1645', 'type': 'B-63'}, {'profile': 'b', 'length': '1670', 'type': 'B-64'}, {'profile': 'b', 'length': '1695', 'type': 'B-65'}, {'profile': 'b', 'length': '1775', 'type': 'B-68'}, {'profile': 'b', 'length': '1850', 'type': 'B-71'}, {'profile': 'b', 'length': '1900', 'type': 'B-73'}, {'profile': 'b', 'length': '1950', 'type': 'B-75'}, {'profile': 'b', 'length': '2025', 'type': 'B-78'}, {'profile': 'b', 'length': '2105', 'type': 'B-81'}, {'profile': 'b', 'length': '2205', 'type': 'B-85'}, {'profile': 'b', 'length': '2330', 'type': 'B-90'}, {'profile': 'b', 'length': '2410', 'type': 'B-93'}, {'profile': 'b', 'length': '2460', 'type': 'B-95'}, {'profile': 'b', 'length': '2510', 'type': 'B-97'}, {'profile': 'b', 'length': '2715', 'type': 'B-105'}, {'profile': 'b', 'length': '2890', 'type': 'B-112'}, {'profile': 'b', 'length': '3095', 'type': 'B-120'}, {'profile': 'b', 'length': '3195', 'type': 'B-124'}, {'profile': 'b', 'length': '3295', 'type': 'B-128'}, {'profile': 'b', 'length': '3500', 'type': 'B-136'}, {'profile': 'b', 'length': '3705', 'type': 'B-144'}, {'profile': 'b', 'length': '4060', 'type': 'B-158'}, {'profile': 'b', 'length': '4160', 'type': 'B-162'}, {'profile': 'b', 'length': '4440', 'type': 'B-173'}, {'profile': 'b', 'length': '4620', 'type': 'B-180'}, {'profile': 'b', 'length': '5000', 'type': 'B-195'}, {'profile': 'b', 'length': '5380', 'type': 'B-210'}, {'profile': 'b', 'length': '5725', 'type': 'B-225'}, {'profile': 'b', 'length': '6105', 'type': 'B-240'}, {'profile': 'b', 'length': '6865', 'type': 'B-270'}, {'profile': 'b', 'length': '7630', 'type': 'B-300'}, {'profile': 'b', 'length': '8390', 'type': 'B-330'}, {'profile': 'b', 'length': '9150', 'type': 'B-360'}, {'profile': 'c', 'length': '1370', 'type': 'C-51'}, {'profile': 'c', 'length': '1470', 'type': 'C-55'}, {'profile': 'c', 'length': '1545', 'type': 'C-58'}, {'profile': 'c', 'length': '1600', 'type': 'C-60'}, {'profile': 'c', 'length': '1675', 'type': 'C-63'}, {'profile': 'c', 'length': '1800', 'type': 'C-68'}, {'profile': 'c', 'length': '1875', 'type': 'C-71'}, {'profile': 'c', 'length': '1900', 'type': 'C-72'}, {'profile': 'c', 'length': '1930', 'type': 'C-73'}, {'profile': 'c', 'length': '1980', 'type': 'C-75'}, {'profile': 'c', 'length': '2130', 'type': 'C-81'}, {'profile': 'c', 'length': '2235', 'type': 'C-85'}, {'profile': 'c', 'length': '2360', 'type': 'C-90'}, {'profile': 'c', 'length': '2510', 'type': 'C-96'}, {'profile': 'c', 'length': '2615', 'type': 'C-100'}, {'profile': 'c', 'length': '2740', 'type': 'C-105'}, {'profile': 'c', 'length': '2920', 'type': 'C-112'}, {'profile': 'c', 'length': '1320', 'type': 'C-120'}, {'profile': 'c', 'length': '3325', 'type': 'C-128'}, {'profile': 'c', 'length': '3530', 'type': 'C-136'}, {'profile': 'c', 'length': '3730', 'type': 'C-144'}, {'profile': 'c', 'length': '4085', 'type': 'C-158'}, {'profile': 'c', 'length': '4190', 'type': 'C-162'}, {'profile': 'c', 'length': '4470', 'type': 'C-173'}, {'profile': 'c', 'length': '4645', 'type': 'C-180'}, {'profile': 'c', 'length': '5025', 'type': 'C-195'}, {'profile': 'c', 'length': '5410', 'type': 'C-210'}, {'profile': 'c', 'length': '5740', 'type': 'C-225'}, {'profile': 'c', 'length': '6120', 'type': 'C-240'}, {'profile': 'c', 'length': '6500', 'type': 'C-255'}, {'profile': 'c', 'length': '6880', 'type': 'C-270'}, {'profile': 'c', 'length': '7645', 'type': 'C-300'}, {'profile': 'c', 'length': '8405', 'type': 'C-330'}, {'profile': 'c', 'length': '9165', 'type': 'C-360'}, {'profile': 'c', 'length': '9930', 'type': 'C-390'}, {'profile': 'c', 'length': '10690', 'type': 'C-420'}, {'profile': 'd', 'length': '3130', 'type': 'D-120'}, {'profile': 'd', 'length': '3335', 'type': 'D-128'}, {'profile': 'd', 'length': '3540', 'type': 'D-136'}, {'profile': 'd', 'length': '3740', 'type': 'D-144'}, {'profile': 'd', 'length': '4095', 'type': 'D-158'}, {'profile': 'd', 'length': '4200', 'type': 'D-162'}, {'profile': 'd', 'length': '4480', 'type': 'D-173'}, {'profile': 'd', 'length': '4655', 'type': 'D-180'}, {'profile': 'd', 'length': '5035', 'type': 'D-195'}, {'profile': 'd', 'length': '5420', 'type': 'D-210'}, {'profile': 'd', 'length': '5735', 'type': 'D-225'}, {'profile': 'd', 'length': '6115', 'type': 'D-240'}, {'profile': 'd', 'length': '6370', 'type': 'D-250'}, {'profile': 'd', 'length': '6880', 'type': 'D-270'}, {'profile': 'd', 'length': '7640', 'type': 'D-300'}, {'profile': 'd', 'length': '8400', 'type': 'D-330'}, {'profile': 'd', 'length': '9165', 'type': 'D-360'}, {'profile': 'd', 'length': '9925', 'type': 'D-390'}, {'profile': 'd', 'length': '10690', 'type': 'D-420'}, {'profile': 'd', 'length': '12210', 'type': 'D-480'})
SuperHC_length = [{'profile': '3v', 'length': '635', 'type': '3V250'}, {'profile': '3v', 'length': '675', 'type': '3V265'}, {'profile': '3v', 'length': '710', 'type': '3V280'}, {'profile': '3v', 'length': '760', 'type': '3V300'}, {'profile': '3v', 'length': '800', 'type': '3V315'}, {'profile': '3v', 'length': '850', 'type': '3V355'}, {'profile': '3v', 'length': '900', 'type': '3V355'}, {'profile': '3v', 'length': '955', 'type': '3V375'}, {'profile': '3v', 'length': '1015', 'type': '3V400'}, {'profile': '3v', 'length': '1080', 'type': '3V425'}, {'profile': '3v', 'length': '1145', 'type': '3V450'}, {'profile': '3v', 'length': '1205', 'type': '3V475'}, {'profile': '3v', 'length': '1270', 'type': '3V500'}, {'profile': '3v', 'length': '1345', 'type': '3V530'}, {'profile': '3v', 'length': '1420', 'type': '3V560'}, {'profile': '3v', 'length': '1525', 'type': '3V600'}, {'profile': '3v', 'length': '1600', 'type': '3V630'}, {'profile': '3v', 'length': '1700', 'type': '3V670'}, {'profile': '3v', 'length': '1805', 'type': '3V710'}, {'profile': '3v', 'length': '1905', 'type': '3V750'}, {'profile': '3v', 'length': '2030', 'type': '3V800'}, {'profile': '3v', 'length': '2160', 'type': '3V850'}, {'profile': '3v', 'length': '2285', 'type': '3V900'}, {'profile': '3v', 'length': '2415', 'type': '3V950'}, {'profile': '3v', 'length': '2540', 'type': '3V1000'}, {'profile': '3v', 'length': '2690', 'type': '3V1060'}, {'profile': '3v', 'length': '2845', 'type': '3V1120'}, {'profile': '3v', 'length': '2995', 'type': '3V1180'}, {'profile': '3v', 'length': '3175', 'type': '3V1250'}, {'profile': '3v', 'length': '3355', 'type': '3V1320'}, {'profile': '3v', 'length': '3555', 'type': '3V1400'}, {'profile': '5v', 'length': '1270', 'type': '5V500'}, {'profile': '5v', 'length': '1345', 'type': '5V530'}, {'profile': '5v', 'length': '1420', 'type': '5V560'}, {'profile': '5v', 'length': '1525', 'type': '5V600'}, {'profile': '5v', 'length': '1600', 'type': '5V630'}, {'profile': '5v', 'length': '1700', 'type': '5V670'}, {'profile': '5v', 'length': '1805', 'type': '5V710'}, {'profile': '5v', 'length': '1905', 'type': '5V750'}, {'profile': '5v', 'length': '2030', 'type': '5V800'}, {'profile': '5v', 'length': '2160', 'type': '5V850'}, {'profile': '5v', 'length': '2285', 'type': '5V900'}, {'profile': '5v', 'length': '2415', 'type': '5V950'}, {'profile': '5v', 'length': '2540', 'type': '5V1000'}, {'profile': '5v', 'length': '2690', 'type': '5V1060'}, {'profile': '5v', 'length': '2845', 'type': '5V1120'}, {'profile': '5v', 'length': '2995', 'type': '5V1180'}, {'profile': '5v', 'length': '3175', 'type': '5V1250'}, {'profile': '5v', 'length': '3355', 'type': '5V1320'}, {'profile': '5v', 'length': '3555', 'type': '5V1400'}, {'profile': '5v', 'length': '3810', 'type': '5V1500'}, {'profile': '5v', 'length': '4065', 'type': '5V1600'}, {'profile': '5v', 'length': '4320', 'type': '5V1700'}, {'profile': '5v', 'length': '4570', 'type': '5V1800'}, {'profile': '5v', 'length': '4825', 'type': '5V1900'}, {'profile': '5v', 'length': '5080', 'type': '5V2000'}, {'profile': '5v', 'length': '5385', 'type': '5V2120'}, {'profile': '5v', 'length': '5690', 'type': '5V2240'}, {'profile': '5v', 'length': '5995', 'type': '5V2360'}, {'profile': '5v', 'length': '6350', 'type': '5V2500'}, {'profile': '5v', 'length': '6730', 'type': '5V2650'}, {'profile': '5v', 'length': '7110', 'type': '5V2800'}, {'profile': '5v', 'length': '7620', 'type': '5V3000'}, {'profile': '5v', 'length': '8000', 'type': '5V3150'}, {'profile': '5v', 'length': '8510', 'type': '5V3350'}, {'profile': '5v', 'length': '9015', 'type': '5V3350'}, {'profile': '8v', 'length': '2540', 'type': '8V1000'}, {'profile': '8v', 'length': '2690', 'type': '8V1060'}, {'profile': '8v', 'length': '2845', 'type': '8V1120'}, {'profile': '8v', 'length': '2995', 'type': '8V1180'}, {'profile': '8v', 'length': '3175', 'type': '8V1250'}, {'profile': '8v', 'length': '3355', 'type': '8V1320'}, {'profile': '8v', 'length': '3555', 'type': '8V1400'}, {'profile': '8v', 'length': '3810', 'type': '8V1500'}, {'profile': '8v', 'length': '4065', 'type': '8V1600'}, {'profile': '8v', 'length': '4320', 'type': '8V1700'}, {'profile': '8v', 'length': '4570', 'type': '8V1800'}, {'profile': '8v', 'length': '4825', 'type': '8V1900'}, {'profile': '8v', 'length': '5080', 'type': '8V2000'}, {'profile': '8v', 'length': '5385', 'type': '8V2120'}, {'profile': '8v', 'length': '5690', 'type': '8V2240'}, {'profile': '8v', 'length': '5995', 'type': '8V2360'}, {'profile': '8v', 'length': '6350', 'type': '8V2500'}, {'profile': '8v', 'length': '6730', 'type': '8V2650'}, {'profile': '8v', 'length': '7110', 'type': '8V2800'}, {'profile': '8v', 'length': '7620', 'type': '8V3000'}, {'profile': '8v', 'length': '8000', 'type': '8V3150'}, {'profile': '8v', 'length': '8510', 'type': '8V3350'}, {'profile': '8v', 'length': '9017', 'type': '8V3550'}, {'profile': '8v', 'length': '9525', 'type': '8V3750'}, {'profile': '8v', 'length': '10160', 'type': '8V4000'}, {'profile': '8v', 'length': '10795', 'type': '8V4250'}, {'profile': '8v', 'length': '11430', 'type': '8V4500'}, {'profile': '8v', 'length': '12065', 'type': '8V4750'}, {'profile': '8v', 'length': '12700', 'type': '8V5000'}, {'profile': '8v', 'length': '14225', 'type': '8V5600'}]



class _Dist(ABC):
    """Abstract class holding private methods to calculate distance properties"""
    def __init__(self, min_diam:float, maj_diam:float):
        self.min_diam = min_diam
        self.maj_diam = maj_diam
        self._c_uc()
        self._l_uc()

    
    def _c_uc(self):
        """Uncorrected center distance"""
        self.center_uncorr = (3 * self.min_diam + self.maj_diam)/2
    

    def _l_uc(self):
        """Uncorrected belt length"""
        self.l_uncorr = 2 * self.center_uncorr + 1.57 * (self.maj_diam + self.min_diam) + ((self.maj_diam - self.min_diam)**2/(4 * self.center_uncorr))


class PulleyBelt(_Dist):
    r"""PulleyBelt class calculates the corrected belt length and the corrected center distance.

    Parameters
    ----------
    min_diam : float
        Smallest pulley, [mm]
    maj_diam : float
        Largest pulley, [mm]
    belt : str
        Belt model, [-]
    b_profile : str
        Belt profile, [-]
    
    Attributes
    ----------
    l_corr : float
        V-Belt corrected length, [mm]
    b_type : str
        V-Belt selected type, [-]
    c_corr : float
        Pulley corrected center length, [mm]


    Notes
    -----
    All the information [#]_ is available online. The valid entries for `belt` and `b_profile` are in the :ref:`Model Profile <vbelt_model_profile>` data section.

    Examples
    --------
    >>> dist = vbelts.length.PulleyBelt(120, 240, 'HiPower', 'a')
    >>> dist.l_c()
    (1200, 'A-46')
    >>> dist.c_c()
    310.72814411208714

    References
    ----------
    .. [#] Claudino Alves, Claudemir. "Transmissão por Correias - Dimensionamento Atividade 2". **Fatec Itaquera**. Accessed September 16, 2020, http://claudemiralves.weebly.com/uploads/3/8/6/2/3862918/dimen._de_correias.pdf.

    """
    def __init__(self, min_diam:float, maj_diam:float, belt:str, b_profile:str, iterator:_ReIterate=_ReIterate, interpol:_Interpolate=_Interpolate):  # inject the objects inside the class
        super().__init__(min_diam, maj_diam)
        self.belt = belt
        self.b_profile = b_profile
        self.iterator = iterator
        self.interpol = interpol
        self.corr_dict = h_factor
        self._l_c()
        self._l_a()
        self._h_factor()


    def _l_c(self):
        """Calculates the corrected v-belt length and type."""
        listname = f'{self.belt}_length'
        self.l_corr, self.b_type = self.iterator(globals()[listname]).belt_type(globals()[listname], self.b_profile, self.l_uncorr)
    

    def l_c(self):
        r"""Belt commercial length and v-belt type.

        Returns
        -------
        result : tuple
            Contains the l_corr and b_type in tuple data form, [-]
        l_corr : float
            Length of the commercial belt chosen, [mm]
        b_type : str
            Commercial v-belt type, [-]

        Notes
        -----
        The return product is a tuple with both values.

        The calculation and selection of the type depends on a number of secundary factors, all available online [#]_.
        First, the pulley center distance uncorrected, `C`, is calculated based on the major `D` and minor `d` pulley diameters:

        .. math::
            C = \frac{3 \cdot d + D}{2}

        Second, the uncorrected length of the belt, `l` is calculated:

        .. math::
            l = 2 \cdot C + 1.57 \cdot (D + d) + \frac{(D - d)**2}{4 \cdot C}

        Third, the corrected commercial length of the v-belt, `l_c` is selected based on the v-belt model and uncorrected length `l`. Please see the :ref:`Data <vbelt_length_data>` for all models in the module.

        References
        ----------
        .. [#] Claudino Alves, Claudemir. "Transmissão por Correias - Dimensionamento Atividade 2". **Fatec Itaquera**. Accessed September 16, 2020, http://claudemiralves.weebly.com/uploads/3/8/6/2/3862918/dimen._de_correias.pdf.
        """
        return (self.l_corr, self.b_type)
    
    
    def _h_factor(self):
        """Calculates and selects the appropriate correction factor for the center distance between pulleys."""
        adim_factor = (self.maj_diam - self.min_diam)/self._l_adj
        for key in self.corr_dict:
            last_factor = 0
            if key == adim_factor:
                self._h = self.corr_dict.get(key)
            elif key > adim_factor:
                self._h = self.interpol(adim_factor, last_factor, key, self.corr_dict.get(last_factor), self.corr_dict.get(key)).y_data()
            last_factor = key
        if self._h is None:
            raise _OutOfRangeError('Value out of range for these parameters')


    def _l_a(self):
        """Corrected belt length for commercial belts."""
        self._l_adj = self.l_corr - 1.57 * (self.maj_diam + self.min_diam)
    

    def c_c(self):
        r"""Corrected pulley center distance for commercial belts.

        Returns
        -------
        c_corr : float
            Corrected center distance between the pulleys, [mm]
        
        Notes
        -----
        The calculation [#]_ demands the adjusted length of the belt, `l_a`, the major pulley diameter `D` and the minor pulley diameter `d`.
        First, the ratio below is calculated:

        .. math::
            \frac{D-d}{l_a}

        Second, from a list of correction factors for center distances, `h` is selected. Please see the :ref:`Data section <vbelt_h_factor_data>` for the complete list.
        Third and finally, the adjusted center distance is defined:

        .. math::
            C_c = \frac{l_a - h \cdot (D - d)}{2}

        References
        ----------
         .. [#] Claudino Alves, Claudemir. "Transmissão por Correias - Dimensionamento Atividade 2". **Fatec Itaquera**. Accessed September 16, 2020, http://claudemiralves.weebly.com/uploads/3/8/6/2/3862918/dimen._de_correias.pdf.
        """
        self.c_corr = (self._l_adj - self._h *(self.maj_diam - self.min_diam))/2
        return self.c_corr
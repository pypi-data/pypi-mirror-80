"""
Length
======
"""

from vbelts.util import _Interpolate, _Iterate, _OutOfRangeError
from abc import ABC

h_factor = {0:0, 0.02:0.01, 0.04:0.02, 0.06:0.03, 0.08:0.04, 0.1:0.05, 0.12:0.06, 0.14:0.07, 0.16:0.08, 0.18:0.09, 0.2:0.1, 0.21:0.11, 0.23:0.12, 0.25:0.13, 0.27:0.14, 0.29:0.15, 0.3:0.16, 0.32:0.17, 0.34:0.18, 0.35:0.19, 0.37:0.2, 0.39:0.21, 0.4:0.22, 0.41:0.23, 0.43:0.24, 0.44:0.25, 0.46:0.26, 0.47:0.27, 0.48:0.28, 0.5:0.29, 0.51:0.3}


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
    def __init__(self, min_diam:float, maj_diam:float, belt:str, b_profile:str, iterator:_Iterate=_Iterate, interpol:_Interpolate=_Interpolate):  # inject the objects inside the class
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
        self.l_corr, self.b_type = self.iterator(f'{self.belt}_length', 'profile', 'length', 'type').belt_type(self.b_profile, self.l_uncorr)
    

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
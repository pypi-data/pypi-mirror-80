"""
Belt
====

"""

from vbelts.util import _Belt, _OutOfRangeError

class HiPower(_Belt):
    r"""HiPower class checks the conditions and selects the v-belt profile for this model.

    Parameters
    ----------
    est_power : float
        estimated power of the system, [hp]
    rpm_fastest : float
        fastest rotational speed of the system, [rpm]
    

    Attributes
    ----------
    profile : str
        Selected v-belt profile, [-]
    

    Examples
    --------
    >>> belt = vbelts.belt.HiPower(3, 500)
    >>> belt.profile
    a
    >>> belt1 = vbelts.belt.HiPower(9, 400)
    >>> betl1.profile
    b


    Notes
    -----
    The data [#]_ is available online.


    References
    ----------
    .. [#] "CLASSICAL," V-Belts, BestTORQ, accessed September 21, 2020,  https://www.bestorq.com/Library/media/CLASSICAL_xselect.gif
    """
    def __init__(self, est_power:float, rpm_fastest:float):
        super().__init__(est_power, rpm_fastest)
        self._boundary_a = super(HiPower, self)._fun_val(74.1950272674027, 47.215442190042, 3322, self.est_power, 50.7)
        self._boundary_b = super(HiPower, self)._fun_val(19.3889694765281, 32.2532889843209, 2151.4, self.est_power, 122.3)
        self._boundary_c = super(HiPower, self)._fun_val(4.94622293507244, 19.7301462298106, 1335.9, self.est_power, 277.35)
        self._belt_profile()
    
    
    def _belt_profile(self):
        r"""Method selects the appropriate profile based on the region limits.
         """
        # Define the maximum range
        if self.rpm_fastest > 5000 or self.est_power > 500:
            return _OutOfRangeError('Values out of range for the HiPower model: rpm > 5000 or est_power > 500')
        elif self.rpm_fastest < 100 or self.est_power < 1:
            return _OutOfRangeError('Values out of range for the HiPower model: rpm < 100 or est_power < 1')

        if self.rpm_fastest >= self._boundary_a:
            profile = 'a'
        elif self._boundary_b <= self.rpm_fastest < self._boundary_a:
            profile = 'b'
        elif self._boundary_c <= self.rpm_fastest < self._boundary_b:
            profile = 'c'
        elif self._boundary_c > self.rpm_fastest:
            profile = 'd'
        self.profile = profile


class SuperHC(_Belt):
    r"""SuperHC class calculates checks the conditions and selects the v-belt profile for this model.

    Parameters
    ----------
    est_power : float
        estimated power of the system, [hp]
    rpm_fastest : float
        fastest rotational speed of the system, [rpm]
    

    Attributes
    ----------
    profile : str
        Selected v-belt profile, [-]
    

    Examples
    --------
    >>> belt = vbelts.belt.SuperHC(4, 1160)
    >>> belt.profile
    3v
    >>> belt1 = vbelts.belt.SuperHC(30, 690)
    >>> betl1.profile
    5v


    Notes
    -----
    The data [#]_ is available online.


    References
    ----------
    .. [#] "WEDGE," V-Belts, BestTORQ, accessed September 21, 2020,  https://www.bestorq.com/Library/media/wedge_xselect358.gif
    """
    def __init__(self, est_power:float, rpm_fastest:float):
        super().__init__(est_power, rpm_fastest)
        self._boundary_3v = super(SuperHC, self)._fun_val(40.6961726224751, 11.8866879052094, 3316.25, self.est_power, 91)
        self._boundary_5v = super(SuperHC, self)._fun_val(4.30114168431602, 3.84423100031302, 1332.74, self.est_power, 309)
        self._belt_profile()

    
    def _belt_profile(self):
        r"""Method selects the appropriate profile based on the region limits.
         """
        # Define the maximum range
        if self.rpm_fastest > 5000 or self.est_power > 1000:
            return _OutOfRangeError('Values out of range for the SuperHC model: rpm > 5000 or est_power > 1000')
        elif self.rpm_fastest < 100 or self.est_power < 1:
            return _OutOfRangeError('Values out of range for the SuperHC model: rpm < 100 or est_power < 1')
        
        if self.rpm_fastest >= self._boundary_3v:
            profile = '3v'
        elif self._boundary_5v <= self.rpm_fastest < self._boundary_3v:
            profile = '5v'
        elif self._boundary_5v > self.rpm_fastest:
            profile = '8v'
        self.profile = profile

"""
Pulley
======
"""

from vbelts.util import _Pulley, _Iterate, _ConvergenceError
from time import time

class Driven(_Pulley):
    r"""Driven class stores essential properties of the driven pulley and calculates driving pulley properties. It also can select the appropriate commercial diameter for the driven pulley, updating the relevant properties like output rpm and gear ratio.

    Parameters
    ----------
    diam : float
        Diameter of the driven pulley, [mm]
    vbelt_profile : str
        Profile of the v-belt, [-]
    power : float
        Power of the system, [hp]
    rpm : float
        Rotational speed of the driven axle, [rpm]
    gear_ratio : float
        Gear ratio of the pulleys in decimal form, [-]
    
    Examples
    --------
    >>> driven_pulley = vbelts.pulley.Driven(240, 'a', 3, 1750, 1.846)
    >>> driven_pulley.driving_pulley()
    130.01083423618635
    >>> driven_pulley.commercial(130, 120)
    [240, 1.8461538461538463, 1750, 947.9166666666666]
    """
    def __init__(self, diam:float, vbelt_profile:str, power:float, rpm:float, gear_ratio:float, iterator:_Iterate=_Iterate):
        super().__init__(diam, vbelt_profile, power, rpm, iterator)
        self.gear_ratio = gear_ratio
    

    def driving_pulley(self):
        r"""Calculated driving pulley diameter.

        Returns
        -------
        driving_diam : float
            Driving pulley diameter, [mm]
        
        Notes
        -----
        The driven gear ratio is calculated [#]_ by:

        .. math::
            D_{driving} = \frac{D_{driven}}{R}
        
        Where the `R` is the gear ratio.

        References
        ----------
        .. [#] Douglas Wright. 2005."DANotes: V-Belt drives: Introduction", **V-BELT DRIVES**. Accessed September 23, 2020, http://www-mdp.eng.cam.ac.uk/web/library/enginfo/textbooks_dvd_only/DAN/V-belts/intro/intro.html.
        """
        return self.diam / self.gear_ratio
    

    def commercial(self, driving_pulley:float, desired_pulley_diam:int):
        r"""Selects an approximate to the commercial diameter of a pulley through iterator convergence.

        Returns
        -------
        result : list
            A list containing the respective results, [-]
        diam_out : float
            Calculated commercial driven pulley diameter, [mm]
        gear_ratio_comm : float
            Calculated gear ratio for the commercial diameter, [-]
        rpm : float
            Input rotational speed, [rpm]
        rpm_out : float
            Calculated output rotational speed for the commercial driven diameter, [rpm]
        """
        # calculate gear ratio range
        range_rpm = 100
        rpm_output = self.rpm/self.gear_ratio
        gear_ratio_max = self.rpm/(rpm_output - range_rpm)
        gear_ratio_min = self.rpm/(rpm_output + range_rpm)
        error_min = 0.01
        driven_pulley = self.gear_ratio * driving_pulley
        diam_calc = driven_pulley

        # _Iterate
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
                raise _ConvergenceError('The function could not reach convergence, try again with a lower value')
        
        # recalculate rpm_output
        base = 10
        diam_out = base * round(diam_calc/base)  # round the number to nearest 5 integer
        gear_ratio_comm = diam_out/driving_pulley
        rpm_out = self.rpm/gear_ratio_comm
        return [diam_out, gear_ratio_comm, self.rpm, rpm_out]



class Driving(_Pulley):
    r"""Driving class stores essential properties of the driving pulley and calculates driven pulley properties.

    Parameters
    ----------
    diam : float
        Diameter of the driving pulley, [mm]
    vbelt_profile : str
        Profile of the v-belt, [-]
    power : float
        Power of the system, [hp]
    rpm : float
        Rotational speed of the driving axle, [rpm]
    gear_ratio : float
        Gear ratio of the pulleys in decimal form, [-]
    
    Examples
    --------
    >>> driving_pulley = vbelts.pulley.Driving(130, 'a', 3, 1000, 1.846)
    >>> driving_pulley.driven_pulley()
    239.98000000000002
    """
    def __init__(self, diam:float, vbelt_profile:str, power:float, rpm:float, gear_ratio:float, iterator:_Iterate=_Iterate):
        super().__init__(diam, vbelt_profile, power, rpm, iterator)
        self.gear_ratio = gear_ratio

    def driven_pulley(self):
        r"""Calculated driven pulley diameter.

        Returns
        -------
        driven_diam : float
            Driven pulley diameter, [mm]
        
        Notes
        -----
        The driven gear ratio is calculated [#]_ by:

        .. math::
            D_{driven} = D_{driving} \cdot R
            
        Where the `R` is the gear ratio.

        References
        ----------
        .. [#] Douglas Wright. 2005."DANotes: V-Belt drives: Introduction", **V-BELT DRIVES**. Accessed September 23, 2020, http://www-mdp.eng.cam.ac.uk/web/library/enginfo/textbooks_dvd_only/DAN/V-belts/intro/intro.html.
        """
        return self.diam * self.gear_ratio
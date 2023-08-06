"""
Power
=====

"""

from vbelts.util import _Iterate, _OutOfRangeError


class EstPower():
    r"""EstPower class calculates the estimated power to run the pulley system.

    Parameters
    ----------
    engine_power : float
        Engine power, [hp]
    drive_group : int
        Engine group classifier, [-]
    machine_group : int
        Machine group classifier, [-]
    hours_service : float
        Amount of hours per day that the system is on, [h]
    
    Attributes
    ----------
    service_factor : float
        Service factor of the system
    
    Notes
    -----
    The service factor data [#]_ is available online.

    Examples
    --------
    >>> est_power = vbelts.power.EstPower(2, 1, 1, 4)
    >>> est_power.calc()
    2
    >>> est_power2 = vbelts.power.EstPower(2, 2, 4, 18)
    >>> est_power2.calc()
    3.6

    References
    ----------
    .. [#] Megadyne. 2016."V-BELTS: Rubber V-belts", **Vermeire webshop**. Accessed September 14, 2020, http://shop.vermeire.com/inc/Doc/courroies/megadyne/2016/v_belts_jan_2016.pdf
    """
    def __init__(self, engine_power:float, drive_group:int, machine_group:int, hours_service:float):
        self.engine_power = engine_power
        self.drive_group = drive_group
        self.machine_group = machine_group
        self.hours_service = hours_service
        self._sf()
    

    def _sf(self):
        r"""Method selects and calculates the service factor.
        """
        # calculate service_factor partial
        if self.machine_group == 1:
            if 0 < self.hours_service <= 5:
                sf_part = 1.0
            elif 5 < self.hours_service <= 10:
                sf_part = 1.1
            elif 10 < self.hours_service <= 24:
                sf_part = 1.2
        elif self.machine_group == 2:
            if 0 < self.hours_service <= 5:
                sf_part = 1.1
            elif 5 < self.hours_service <= 10:
                sf_part = 1.2
            elif 10 < self.hours_service <= 24:
                sf_part = 1.3
        elif self.machine_group == 3:
            if 0 < self.hours_service <= 5:
                sf_part = 1.2
            elif 5 < self.hours_service <= 10:
                sf_part = 1.3
            elif 10 < self.hours_service <= 24:
                sf_part = 1.4
        elif self.machine_group == 4:
            if 0 < self.hours_service <= 5:
                sf_part = 1.3
            elif 5 < self.hours_service <= 10:
                sf_part = 1.4
            elif 10 < self.hours_service <= 24:
                sf_part = 1.5
        # calculate service_factor additional and final
        if self.machine_group == 1 and self.drive_group == 2:
            result = sf_part + 0.1
        elif self.machine_group == 2 and self.drive_group == 2:
            result = sf_part + 0.1
        elif self.machine_group == 3 and self.drive_group == 2:
            if sf_part == 1.4:
                result = sf_part + 0.1
            else:
                result = sf_part + 0.2
        elif self.machine_group == 4 and self.drive_group == 2:
            if sf_part == 1.4:
                result = sf_part + 0.2
            else:
                result = sf_part + 0.3
        else:
            result = sf_part
        self._service_factor = round(result,1)

    
    def calc(self):
        r"""Estimated power to run the pulley system.

        Returns
        -------
        pp : float
            Estimated power, [hp]
        
        Notes
        -----
        The equation to calculate the estimated power, using the engine power `P_{engine}` and the service factor `F_s`:

        .. math::
            P_p = P_{engine} \cdot F_s
        """
        pp = self.engine_power * self._service_factor
        return pp


class TransPower():
    """TransPower class calculates the quantity of belts needed to ensure the power of the system.

    Parameters
    ----------
    vbelt_model : str
        Model of the v-belt, [-]
    vbelt_profile : str
        Profile of the v-belt, [-]
    vbelt_type : str
        Type of the v-belt, [-]
    est_power : float
        Estimated power, [hp]
    gear_ratio : float
        Pulley system gear ratio, [-]
    belt_length_corr : float
        Corrected belt length, [-]
    min_diam : float
        Smallest pulley, [mm]
    maj_diam : float
        Largest pulley, [mm]
    rpm : float
        Fastest axle rotation speed, [rpm]
    
    Notes
    -----
    All the information [#]_ is available online. The valid entries for `vbelt_model`, `vbelt_profile` and `vbelt_type` are in the :ref:`Model Profile <vbelt_model_profile>` and in the :ref:`Types <vbelt_types>` of the data section.

    Examples
    --------
    >>> trans_power = vbelts.power.TransPower('HiPower', 'a', 'A-32', 2, 130/240, 850, 130, 240, 1750)
    >>> trans_power.calc()
    0.5060451558976288

    References
    ----------
    .. [#] Claudino Alves, Claudemir. "Transmissão por Correias - Dimensionamento Atividade 2". **Fatec Itaquera**. Accessed September 16, 2020, http://claudemiralves.weebly.com/uploads/3/8/6/2/3862918/dimen._de_correias.pdf.
    """
    def __init__(self, vbelt_model:str, vbelt_profile:str, vbelt_type:str, est_power:float, gear_ratio:float, belt_length_corr:float, min_diam:float, maj_diam:float, rpm:float, iterator:_Iterate=_Iterate):
        self.b_model = vbelt_model
        self.b_profile = vbelt_profile
        self.b_type = vbelt_type
        self.est_power = est_power
        self.gear_ratio = gear_ratio
        self.l_corr = belt_length_corr
        self.min_diam = min_diam
        self.maj_diam = maj_diam
        self.rpm = rpm
        self.iterator = iterator
        self._fc_length()
        self._basic()
        self._additional()
        self._fc_arc()
    

    def _fc_length(self):
        """Selects the appropriate correction factor for belt length."""
        filename_fcc = f'{self.b_model}_fcc'
        for line in self.iterator(filename_fcc).read():
            if line['type'] == self.b_type:
                self._fcc = float(line['fcc'])
    

    def _basic(self):
        """Select the basic power transmitted by belt unit."""
        filename_pb = f'{self.b_model}_{self.b_profile}_pb'
        temp_result, adjust = self.iterator(filename_pb, 'diameter', 'rpm', 'power_b').three_rows(self.min_diam, self.rpm)
        # result adjusting for interpolation
        if adjust:
            if 0.3 < temp_result <= 1:
                self._p_basic = temp_result - 0.25
            elif 1 < temp_result <= 10:
                self._p_basic = temp_result - 0.5
            elif 10 < temp_result <= 120:
                self._p_basic = temp_result - 2.5
        else:
            self.p_basic = temp_result
    

    def _additional(self):
        """Selects the additional power transmitted by belt unit."""
        filename_pa = f'{self.b_model}_{self.b_profile}_pa'
        # checking if gear_ratio is below one and adjust
        if self.gear_ratio < 1:
            gear_ratio_corr = 1/self.gear_ratio
        else:
            gear_ratio_corr = self.gear_ratio
        self._p_add = self.iterator(filename_pa, 'gr_low', 'gr_high', 'rpm', 'power_a').four_rows(gear_ratio_corr, self.rpm)


    def _fc_arc(self):
        """Selects the appropriate correction factor for contact arc."""
        factor = (self.maj_diam - self.min_diam) / self.l_corr
        self._fcac = self.iterator('fcac_contact_arc', 'factor', 'contact_arc', 'fcac').three_rows_choose(factor, 3)


    def belt_qty(self):
        r"""Number of v-belts needed to transmit the estimated power.

        Returns
        -------
        b_qty : float
            Quantity of v-belts, [-]
        

        Notes
        -----
        Before calculate the belt quantity, the transmitted power `P_t` in horse-power has to be calculated [#]_ by:

        .. math::
            P_t = (P_b + P_a) \cdot f_{cc} \cdot f_{cac}

        Where `P_b` is the basic power transmitted, `P_a` is the additional power transmitted, `f_{cc}` is the length correction factor and `f_{cac}` is the contact arc correction factor.
        Then, the belt quantity is calculated by:

        .. math::
            N_{v-belt} = \frac{P_{estimated}}{P_t}

        References
        ----------
        .. [#] Claudino Alves, Claudemir. "Transmissão por Correias - Dimensionamento Atividade 2". **Fatec Itaquera**. Accessed September 16, 2020, http://claudemiralves.weebly.com/uploads/3/8/6/2/3862918/dimen._de_correias.pdf.
        """
        belt_transmission_capacity = (self._p_basic + self._p_add) * self._fcc * self._fcac
        return self.est_power / belt_transmission_capacity

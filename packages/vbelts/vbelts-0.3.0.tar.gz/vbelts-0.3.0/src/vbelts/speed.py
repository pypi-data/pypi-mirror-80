"""
Speed
=====
"""
from math import pi

def peripheral(pulley_diam:float, pulley_rpm:float):
    r"""Mean peripheral linear velocity of the v-belt.


    Parameters
    ----------
    pulley_diam : float
        mean diameter of the pulley, [mm]
    pulley_rpm : float
        rotational speed of the pulley, [rpm]
    
    Returns
    -------
    v_peripheral : float
        Linear velocity of the v-belt, [m/s]
    

    Examples
    --------
    >>> vbelts.speed.peripheral(240, 1750):
    21.99114857512855


    Notes
    -----
    The velocity is defined [#]_ as:

    .. math::
        v_p &= \omega \cdot r \\
        v_p &= \frac{\pi \cdot r \cdot n}{30}


    References
    ----------
    .. [#] Claudino Alves, Claudemir. "Transmissão por Correias - Dimensionamento Atividade 2". **Fatec Itaquera**. Accessed September 16, 2020, http://claudemiralves.weebly.com/uploads/3/8/6/2/3862918/dimen._de_correias.pdf
    """
    pulley_diam_m = pulley_diam/1000
    return (pi * (pulley_diam_m/2) * pulley_rpm)/30
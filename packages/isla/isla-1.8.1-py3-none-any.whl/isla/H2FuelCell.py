import numpy as np

from .SupplementaryComponent import SupplementaryComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class H2FuelCell(SupplementaryComponent):
    """Hydrogen fuel cell module.

    Parameters
    ----------
    capex : float or callable
        Capital expenses [$/kW(h)]. Depends on size. Can be a callable
        function that returns capital cost starting from year zero to end of
        project lifetime.
    opex_fix : float or callable
        Fixed yearly operating expenses [$/kW(h) yr]. Depends on size. Can be
        a callable function that returns the fixed operating cost starting
        from year zero to end of project lifetime.
    opex_var : float or callable
        Variable yearly operating expenses [$/kWh yr]. Depends on energy
        produced. Can be a callable function that returns the variable
        operating cost starting from year zero to end of project lifetime.
    opex_use : float or callable
        Variable yearly operating expenses [$/h yr]. Depends on amount of
        usage. Can be a callable function that returns the variable
        operating cost starting from year zero to end of project lifetime.
    life : float
        Lifetime [y] of the component.
    life_use : float or None
        Lifetime based on usage [h].

    Other Parameters
    ----------------
    repex : float or callable
        Replacement costs [USD/kW(h)]. Depends on size. Equal to CapEx by
        default. Can be a callable function that returns replacement costs
        starting from year zero to end of project lifetime.
    num_case : int
        Number of scenarios to simultaneously simulate. This is set by the
        Control module.
    size : int
        Size of the component [kW]. This is set by the Control module.

    Notes
    -----
    This module models only the discharging power [kW] of the hydrogen system.
    A H2Storage and H2Electrolyzer module should also be initialized to model\
    the energy [kWh] and charge power respectively.

    """

    def __init__(
        self, capex=6500.0, opex_fix=65.0, opex_var=0.0, opex_use=0.0,
        life=10.0, life_use=None, **kwargs
    ):
        """Initializes the base class."""

        # initialize component
        super().__init__(
            None, capex, opex_fix, opex_var, opex_use,
            'H2 Fuel Cell', None, None, None,
            life, 0.0, False, True, True, False, **kwargs
        )

        # get fuel cell parameters
        self.p_h2 = kwargs.pop('p_h2', 1.32)  # H2 pressure [bar]
        self.p_o2 = kwargs.pop('p_o2', 0.213)  # H2 pressure [bar]
        self.temp = kwargs.pop('temp', 338.15)  # temp [K]
        self.size_nom = kwargs.pop('size_nom', 1.2)  # nominal size [kW]

        # initialize fuel cell parameters
        self.ocv = 0
        self.taf_a = 0
        self.taf_b = 0
        self.res = 0
        self.num_batt = np.array([])

        # adjustable fuel cell parameters
        self.life_use = life_use  # hours of operation before replacement [h]

        # derivable fuel cell parameters
        self.ocv = (
            1.229-8.45e-4*(self.temp-298.15) +
            4.31e-5*self.temp*np.log(self.p_h2*np.sqrt(self.p_o2))
        )*36
        self.taf_a = 0.6259-1.1128e-3*self.temp
        self.taf_b = 0.091487-1.4866e-4*self.temp
        self.res = 2.8959e-3-4.8479e-6*self.temp

        # update initialized parameters if essential data is complete
        self._update_init()

    def cost_calc(self, yr_proj, disc):
        """Returns the costs of the component.

        Parameters
        ----------
        yr_proj : float
            Project lifetime [yr].
        disc : float
            Discount rate.

        Returns
        -------
        cost_c : ndarray
            Total capital cost [$] of the component.
        cost_of : ndarray
            Total fixed operating cost [$] of the component.
        cost_ov : ndarray
            Total variable operating cost [$] of the component.
        cost_ou : ndarray
            Total usage operating cost [$] of the component.
        cost_r : ndarray
            Total replacement cost [$] of the component.
        cost_f : ndarray
            Total fuel cost of the component [$]

        Notes
        -----
        This function can be modified by the user.

        """
        # calculate replacement period
        if self.life_use is None:
            rep_per = self.life
        elif self.life is None:
            rep_per = self.life_use/self.use_tot
        else:
            rep_per = np.minimum(self.life, self.life_use/self.use_tot)

        # calculate other costs
        cost_c = self.capex_calc(yr_proj)
        cost_of = self.opex_fix_calc(yr_proj, disc)
        cost_ov = self.opex_var_calc(yr_proj, disc)
        cost_ou = self.opex_use_calc(yr_proj, disc)
        cost_r = self.repex_calc(yr_proj, disc, rep_per)

        return (cost_c, cost_of, cost_ov, cost_ou, cost_r, 0)

    def update_init(self):
        """Updates other parameters once essential parameters are complete."""

        # calculate number of units
        self.num_batt = self.size/self.size_nom

    @staticmethod
    def exp_curve(yr, yr_0=2016, **kwargs):
        """Experience curve for Solar PV.
        Returns the cost [USD/kW] at the given year.

        Parameters
        ----------
        yr : int
            Index of the year.
        yr_0 : int
            Year where index is set to zero.

        """
        # get regression parameters
        a_sat = kwargs.pop('a_sat', 97)
        a_base = kwargs.pop('a_base', 0.05)
        r = kwargs.pop('r', 0.5)
        a = kwargs.pop('a', 8361)
        b = kwargs.pop('b', 0.287)

        # calculate cost [USD/kWh]
        cap = a_sat/(1+(a_sat-a_base)/a_base*np.exp(-r*(yr+(yr_0-2013))))
        cost = a*cap**(-b)

        return cost

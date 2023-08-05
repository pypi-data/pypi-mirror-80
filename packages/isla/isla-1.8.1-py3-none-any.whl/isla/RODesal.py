import numpy as np

from .SinkComponent import SinkComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class RODesal(SinkComponent):
    """Reverse Osmosis.

    Parameters
    ----------
    data : ndarray
        Dataset. Set to zero if no dataset is required.
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
    name_solid : str
        Label used for the power output. Appears as a solid area in powerflows
        and as a header in .csv files. Usually the name of the component.
    color_solid : str
        Hex code (e.g. '#33CC33') of the color corresponding to name_solid.
        Appears in the solid area in powerflows.
    name_line : str
        Label used for the power output. Appears as a line in powerflows
        and as a header in .csv files. Usually the name of a Load component or
        Storage state of charge.
    color_line : str
        Hex code (e.g. '#33CC33') of the color corresponding to name_line.
        Appears in the line in powerflows.
    life : float
        Lifetime [y] of the component.
    fail_prob : float
        Probability of failure of the component.
    is_fail : bool
        True if failure probabilities should be simulated.
    is_re : bool
        True if the resource is renewable.

    Other Parameters
    ----------------
    repex : float or callable
        Replacement costs [$/kW(h)]. Depends on size. Equal to CapEx by
        default. Can be a callable function that returns replacement costs
        starting from year zero to end of project lifetime.
    num_case : int
        Number of scenarios to simultaneously simulate. This is set by the
        Control module.
    size : int
        Size of the component [kW]. This is set by the Control module.

    """

    def __init__(
        self, ld_module, st_module, capex=6896.55, opex_fix=0.0,
        opex_var=0.232, opex_use=0.0, life=6.0, td=0.33, ru=0,
        enr_el=4.35, is_sink=False, **kwargs
    ):
        """Initializes the base class."""

        # initialize component
        super().__init__(
            None, capex, opex_fix, opex_var, opex_use,
            'RO Desal', '#0000FF', None, None,
            life, 0.0, False, True, False, True, **kwargs
        )

        # get storage and module
        self.st_module = st_module
        self.ld_module = ld_module

        # get parameters
        self.td = td  # turndown ratio
        self.ru = ru  # ramp up ratio
        self.enr_el = enr_el  # energy intensity
        self.is_sink = is_sink  # True if functions as sink only

        # update initialized parameters if essential data is complete
        self._update_init()

    def calc_pow(self, pow_req, n):
        """Returns the power output [kW] of the component given the minimum
        required power [kW] and timestep.

        Parameters
        ----------
        pow_req : ndarray
            Minimum required power [kW].
        n : int
            Time in the simulation.

        Returns
        -------
        pow_gen : ndarray
            The power output [kW] of the component.

        Notes
        -----
        This function can be modified by the user.

        """
        # get upper and lower limits
        ub = self.size*(1+self.ru)
        lb = self.size*self.td

        # get power that can be input
        pow_in = np.minimum(pow_req, ub)
        pow_in[pow_req < lb] = 0

        return pow_in

    def rec_pow(self, pow_rec, n):
        """Records parameters at the specified time step.

        Parameters
        ----------
        pow_rec : ndarray
            Power [kW] to be recorded by component.
        n : int
            Time in the simulation.

        Notes
        -----
        This function can be modified by the user.

        """
        # consume water
        wat_req = self.ld_module.water[n]
        self.st_module.soc -= wat_req*self.dt/self.st_module.size
        self.st_module.soc[self.st_module.size == 0] = 0  # error handling

        # check if water has to be generated
        pow_req = self.enr_el*np.maximum(
            self.st_module.size*(self.st_module.lvl_min-self.st_module.soc),
            0  # if SOC > min water level, do not force generation
        )/self.dt
        pow_req[self.st_module.size == 0] = wat_req*self.enr_el
        pow_req = np.maximum(pow_req, self.size*self.td)
        self.ld_module.pow = pow_req

        # update water level
        pow_tot = np.minimum(pow_req+pow_rec, self.size)  # additional water
        pow_use = np.minimum(
            (1-self.st_module.soc)*self.enr_el*self.st_module.size/self.dt,
            pow_tot
        )
        pow_use[self.st_module.size == 0] = wat_req*self.enr_el
        self.st_module.soc += pow_tot*self.dt/(
            self.enr_el*self.st_module.size
        )
        self.st_module.soc = np.minimum(self.st_module.soc, 1)
        self.st_module.soc[self.st_module.size == 0] = 0
        self.ld_module.enr_tot += pow_tot*self.dt

        # zero sizes
        self.ld_module.pow[self.st_module.size == 0] = np.nan
        self.ld_module.pow[self.size == 0] = np.nan

        # strictly sink component
        if self.is_sink:
            self.ld_module.pow[pow_req > 0] = np.nan

    def opex_var_calc(self, yr_proj, disc):
        """Default method of solving variable operating costs.

        Parameters
        ----------
        yr_proj : float
            Project lifetime [yr].
        disc : float
            Discount rate.

        Returns
        -------
        cost_ov : ndarray
            Total variable operating cost [$] of the component.

        """
        # fixed operating costs [USD], size [kW] based
        yr = np.arange(0, yr_proj+1)
        yr_sc = 8760/(self.nt*self.dt)  # scale factor
        if callable(self.opex_var):
            opex = self.opex_var(yr)/(1+disc)**yr
        else:
            opex = self.opex_var/(1+disc)**yr

        # opex array
        opex_arr = np.repeat(np.atleast_2d(opex).T, self.num_case, axis=1)
        opex_arr[0, :] = 0
        cost_ov = self.ld_module.enr_tot/self.enr_el*yr_sc*opex_arr

        return cost_ov

    def update_init(self):
        """Updates other parameters once essential parameters are complete.

        """
        pass

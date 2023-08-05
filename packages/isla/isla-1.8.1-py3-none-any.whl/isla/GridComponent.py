from abc import abstractmethod

import numpy as np

from .Component import Component

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class GridComponent(Component):
    """Base class for grid power components.

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
    opex_ret : float or callable
        Savings per unit energy returned to grid [$/kWh yr]. Can be a callable
        function that returns the variable operating cost starting from year\
        zero to end of project lifetime.
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
    is_elec : bool
        True if the resource is electrical.
    is_water : bool
        True if the resource is water.

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
        self, data, capex, opex_fix, opex_var, opex_ret, opex_use,
        name_solid, color_solid, name_line, color_line,
        life, fail_prob, is_fail, is_re, is_elec, is_water,
        **kwargs
    ):
        """Initializes the base class."""

        # initialize component
        super().__init__(
            data, capex, opex_fix, opex_var, opex_use,
            name_solid, color_solid, name_line, color_line,
            life, fail_prob, is_fail, is_re, is_elec, is_water
        )

        # store economic parameters
        self.opex_ret = opex_ret

        # initialize grid parameters
        self.pow_ret = np.array([])  # power for net metering [kW]
        self.enr_ret = np.array([])  # energy for net metering [kWh]

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
        cost_r : ndarray
            Total replacement cost [$] of the component.
        cost_f : ndarray
            Total fuel cost of the component [$]

        Notes
        -----
        This function can be modified by the user.

        """
        def ann_func(i):
            """Annunity factor"""
            return 1/(1+disc)**i

        # use defaults for capex, fixed opex, replacement
        cost_c = self.capex_calc(yr_proj)
        cost_of = self.opex_fix_calc(yr_proj, disc)
        cost_ou = self.opex_use_calc(yr_proj, disc)
        cost_r = self.repex_calc(yr_proj, disc, self.life)

        # initialize
        yr = np.arange(1, yr_proj+1)
        yr_sc = 8760/(self.nt*self.dt)  # scale factor

        # variable operating costs, usage
        if callable(self.opex_fix):
            opex = self.opex_var(yr)/(1+disc)**yr
        else:
            opex = self.opex_var/(1+disc)**yr

        # opex array
        opex_arr = np.repeat(np.atleast_2d(opex).T, self.num_case, axis=0)
        opex_arr[0, :] = 0
        cost_ov_use = self.enr_tot*yr_sc*opex_arr

        # variable operating costs, net metering
        if callable(self.opex_fix):
            opex = self.opex_ret(yr)/(1+disc)**yr
        else:
            opex = self.opex_ret/(1+disc)**yr

        # opex array
        opex_arr = np.repeat(np.atleast_2d(opex).T, self.num_case, axis=0)
        opex_arr[0, :] = 0
        cost_ov_ret = self.enr_ret*yr_sc*opex_arr

        # total variable operating cost
        cost_ov = cost_ov_use-cost_ov_ret

        return (cost_c, cost_of, cost_ov, cost_ou, cost_r, 0)

    def _rec_pow(self, pow_rec, n):
        """Records the power at a specified time step.

        Parameters
        ----------
        pow_rec : ndarray
            Power [kW] to be recorded by component.
        n : int
            Time in the simulation.

        """
        # record power
        self.use_tot += pow_rec != 0

        # failure probability
        if not self.is_fail:
            noise = 1
        else:
            noise = np.random.rand(self.num_case) > self.fail_prob
        self.noise = noise
        pow_rec = pow_rec*noise

        # record additional parameters
        self.rec_pow(pow_rec, n)

        # record power
        self.pow = pow_rec*(pow_rec >= 0)
        self.enr_tot += pow_rec*(pow_rec >= 0)*self.dt
        self.pow_ret = -pow_rec*(pow_rec < 0)
        self.enr_ret += -pow_rec*(pow_rec < 0)*self.dt

    @abstractmethod  # implementation required
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
        pass

    def _update_init(self):
        """Updates initialized parameters once size and num_case are given."""

        # check if all essential parameters are in
        if (
            self.num_case is not None and
            self.size is not None and
            self.nt is not None
        ):

            # prevents optimization errors
            if self.size.size == self.num_case:

                # update component parameters
                self.pow = np.zeros(self.num_case)  # instantaneous power [kW]
                self.enr_tot = np.zeros(self.num_case)  # tot energy out [kWh]
                self.use_tot = np.zeros(self.num_case)  # tot energy out [kWh]
                self.pow_ret = np.zeros(self.num_case)  # power for net mt [kW]
                self.enr_ret = np.zeros(self.num_case)  # enr for net mt [kWh]
                self.noise = np.ones(self.num_case)

                # update cost parameters
                self.cost_c = np.zeros(self.num_case)  # capital cost [$]
                self.cost_of = np.zeros(self.num_case)  # fixed opex [$]
                self.cost_ov = np.zeros(self.num_case)  # var opex [$]
                self.cost_ou = np.zeros(self.num_case)  # use opex [$]
                self.cost_r = np.zeros(self.num_case)  # replacement cost [$]
                self.cost_f = np.zeros(self.num_case)  # fuel cost [$]
                self.cost = np.zeros(self.num_case)  # total cost [$]

                # update other parameters
                self.update_init()

    @abstractmethod  # implementation required
    def update_init(self):
        """Updates other parameters once essential parameters are complete.

        """
        pass

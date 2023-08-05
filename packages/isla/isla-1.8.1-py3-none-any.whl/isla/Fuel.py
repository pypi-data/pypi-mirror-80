from abc import abstractmethod

import numpy as np

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class Fuel(object):
    """Base class for fuel.

    Parameters
    ----------
    cost : float or callable
        Cost per unit [$/u] of fuel. Can be a callable function that returns
        fuel cost starting from year zero to end of project lifetime.
    fl_infl : float
        Inflation rate of fuel.
    den : float
        Mass per unit [kg/u] of the fuel.
    lhv : float
        Lower heating value [MJ/kg] of the fuel.
    cost_ret : float or callable
        Savings per unit [$/u] of fuel produced. Can be a callable function
        that returns fuel cost starting from year zero to end of project
        lifetime.
    name_solid : str
        Label used for the power output. Appears as a solid area in powerflows
        and as a header in .csv files. Usually the name of the component.
    color_solid : str
        Hex code (e.g. '#33CC33') of the color corresponding to name_solid.
        Appears in the solid area in powerflows.
    is_re : bool
        True if the resource is renewable.

    """

    def __init__(
        self, cost, fl_infl, den, lhv, cost_ret,
        name_solid, color_solid, is_re
    ):
        """Initializes the base class."""

        # store fuel parameters
        self.cost = cost
        self.fl_infl = fl_infl
        self.den = den  # density
        self.lhv = lhv  # LHV
        self.cost_ret = cost_ret  # savings
        self.name_solid = name_solid  # name on plot
        self.color_solid = color_solid  # color on plot
        self.is_re = is_re  # True if renewable

        # initialize fuel parameters
        self.fl_tot = 0  # total fuel used
        self.fl_ret = 0  # total fuel created
        self.fl_use = 0  # times that fuel is used
        self.cost_f = 0  # total cost of fuel
        self.num_case = None  # number of cases to simu

        # initialize timestep parameters
        self.dt = 0  # timestep
        self.t_span = 0  # length of simulation
        self.nt = None  # number of simulation points

    def _set_num(self, num_case):
        """Changes the number of cases to simulate. Used by the Control module.

        Parameters
        ----------
        num_case : int
            Number of scenarios to simultaneously simulate. This is set by the
            Control module.

        """
        # set number of cases
        self.num_case = num_case
        self.fl_tot = np.zeros(num_case)  # total fuel used
        self.fl_ret = np.zeros(num_case)  # total fuel created
        self.fl_use = np.zeros(num_case)  # times that fuel is used
        self.cost_f = np.zeros(num_case)  # total cost of fuel

    def _set_time(self, dt, t_span):
        """Changes the timestep of the components. Used by the Control module.

        Parameters
        ----------
        dt : float
            Size of one timestep [h]

        """
        # set timestep
        self.dt = dt
        self.t_span = t_span
        self.nt = int(np.ceil(t_span/dt))

    def _rec_fl(self, fl_rec, n):
        """Records fuel use at a specified time step.

        Parameters
        ----------
        fl_rec : ndarray
            Fuel use [u] to be recorded.
        n : int
            Time in the simulation.

        """
        # record additional parameters
        self.rec_fl(fl_rec, n)

        # record fuel used
        self.fl_tot += fl_rec*(fl_rec > 0)*self.dt
        self.fl_ret += fl_rec*(fl_rec < 0)*self.dt
        self.fl_use += fl_rec != 0

    @abstractmethod
    def rec_fl(self, fl_rec, hr):
        """Records fuel use at a specified time step.

        Parameters
        ----------
        fl_rec : ndarray
            Fuel use [u] to be recorded.
        hr : int
            Time [h] in the simulation.

        """
        pass

    def _cost_calc(self, yr_proj, disc):
        """Calculates the cost of fuel.

        Parameters
        ----------
        yr_proj : float
            Project lifetime [yr].
        disc : float
            Discount rate.

        """
        # calculate costs
        self.cost_f = self.cost_calc(yr_proj, disc)

    def fl_use_calc(self, yr_proj, disc):
        """Default method of solving fuel use costs.

        Parameters
        ----------
        yr_proj : float
            Project lifetime [yr].
        disc : float
            Discount rate.

        """
        # fixed operating costs [USD], size [kW] based
        yr = np.arange(0, yr_proj+1)
        yr_sc = 8760/(self.nt*self.dt)  # scale factor
        if callable(self.cost):
            fc = self.cost(yr)*((1+self.fl_infl)/(1+disc))**yr
        else:
            fc = self.cost*((1+self.fl_infl)/(1+disc))**yr

        # fuel cost array
        fc_arr = np.repeat(np.atleast_2d(fc).T, self.num_case, axis=1)
        fc_arr[0, :] = 0
        cost_f = self.fl_tot*yr_sc*fc_arr

        return cost_f

    def fl_ret_calc(self, yr_proj, disc):
        """Default method of solving fuel production savings.

        Parameters
        ----------
        yr_proj : float
            Project lifetime [yr].
        disc : float
            Discount rate.

        """
        # fixed operating costs [USD], size [kW] based
        yr = np.arange(0, yr_proj+1)
        yr_sc = 8760/(self.nt*self.dt)  # scale factor
        if callable(self.cost_ret):
            fc = self.cost_ret(yr)*((1+self.fl_infl)/(1+disc))**yr
        else:
            fc = self.cost_ret*((1+self.fl_infl)/(1+disc))**yr

        # fuel cost array
        fc_arr = np.repeat(np.atleast_2d(fc).T, self.num_case, axis=1)
        fc_arr[0, :] = 0
        save_f = self.fl_ret*yr_sc*fc_arr

        return save_f

    def cost_calc(self, yr_proj, disc):
        """Calculates the cost of fuel.

        Parameters
        ----------
        yr_proj : float
            Project lifetime [yr].
        disc : float
            Discount rate.

        Notes
        -----
        This function can be modified by the user.

        """
        cost_f = self.fl_use_calc(yr_proj, disc)
        save_f = self.fl_ret_calc(yr_proj, disc)

        return cost_f-save_f

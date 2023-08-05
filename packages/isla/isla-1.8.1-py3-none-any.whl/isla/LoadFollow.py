import numpy as np

from .Dispatch import Dispatch


class LoadFollow(Dispatch):
    """Load Following dispatch strategy.

    Parameters
    ----------
    comp_list : list of Component
        List of initialized components.
    size : dict
        Sizes [kW] or [kWh] of the components. Use component objects as
        keys and sizes as values.
    spin_res : float
        Spinning reserve on top of load.
    tol : float
        Tolerance.

    """

    def __init__(self, comp_list, dt, t_span, size, spin_res, tol=1e-2):
        """Initializes the base class."""

        # initialize superclass
        super().__init__(comp_list, dt, t_span, size, spin_res, tol)

    def step(self, pow_ld):
        """Dispatch algorithm.

        Parameters
        ----------
        pow_ld : ndarray
            The load that needs to be served.

        Returns
        -------
        im_pow : ndarray
            Power given by intermittent sources.
        st_c : ndarray
            Charging into energy storage.
        st_dc : ndarray
            Discharging from energy storage.
        dp_pow : ndarray
            Power given by dispatchable sources.
        sk_pow : ndarray
            Power given to load sink.
        gd_c : ndarray
            Power given back to the grid.
        gd_dc : ndarray
            Power drawn from the grid.

        """

        # get intermittent power and load
        pow_im = self.im._get_pow(self.n)

        # case 0: intermittent power does not supply load
        # case 1: intermittent power supplies load
        case0 = pow_im < pow_ld
        case1 = pow_im >= pow_ld

        # 1: determine power for charging storage
        pow_c = pow_im-pow_ld

        # case 10: storage is not fully charged
        # case 11: storage is fully charged
        case10 = np.logical_and(
            case1,
            np.logical_not(self.st.is_full)
        )
        case11 = np.logical_and(
            case1,
            self.st.is_full
        )

        # get power that can enter sink
        pow_skmax = self.sk.pow_max

        # case 110: sink does not absorb all the power
        # case 111: sink absorbs all the power
        case110 = np.logical_and(
            case11,
            pow_skmax < pow_c
        )
        case111 = np.logical_and(
            case11,
            pow_skmax >= pow_c
        )

        # 110: determine power for net metering
        gdc110 = case110*(pow_c-pow_skmax)
        sk110 = case110*pow_skmax

        # 111: give power to sink
        sk111 = case111*pow_c

        # determine maximum charge rate
        pow_maxc = self.st.pow_maxc

        # case 100: not beyond max charge
        # case 101: beyond max charge
        case100 = np.logical_and(
            case10,
            pow_c <= pow_maxc
        )
        case101 = np.logical_and(
            case10,
            pow_c > pow_maxc
        )

        # 100: determine power for charging
        stc100 = case100*pow_c

        # 101: max charge then give excess to sink
        stc101 = case101*pow_maxc

        # case 1010: sink does not absorb all the power
        # case 1011: sink absorbs all the power
        case1010 = np.logical_and(
            case101,
            pow_skmax < pow_c-pow_maxc
        )
        case1011 = np.logical_and(
            case101,
            pow_skmax >= pow_c-pow_maxc
        )

        # 110: determine power for net metering
        gdc1010 = case1010*(pow_c-pow_maxc-pow_skmax)
        sk1010 = case1010*pow_skmax

        # 111: give power to sink
        sk1011 = case1011*(pow_c-pow_maxc)

        # 0: calculate combined power of intermittent and storage
        pow_stmax = self.st.pow_maxdc
        pow_ismax = pow_im+pow_stmax

        # case 00: intermittent + storage cannot supply load
        # case 01: intermittent + storage can supply load
        case00 = np.logical_and(
            case0,
            pow_ismax < pow_ld
        )
        case01 = np.logical_and(
            case0,
            pow_ismax >= pow_ld
        )

        # 01: lower discharge from storage
        std01 = case01*(pow_ld-pow_im)

        # 00: run dispatchable resource
        pow_dpreq = pow_ld-pow_ismax  # required power
        pow_dp = self.dp._calc_pow(pow_dpreq, self.n)  # output power
        dp00 = case00*pow_dp

        # case 000: intermittent, storage, and disp do not suffice
        # case 001: intermittent, storage, and disp suffice
        case000 = np.logical_and(
            case00,
            pow_ld > (pow_ismax+pow_dp)
        )
        case001 = np.logical_and(
            case00,
            pow_ld <= (pow_ismax+pow_dp)
        )

        # 000: discharge storage
        std000 = case000*pow_stmax

        # 000: use grid
        gdd000 = case000*(pow_ld-(pow_ismax+pow_dp))

        # 001: lower storage discharge so that output just meets load
        pow_st = pow_ld-(pow_im+pow_dp)

        # case 0010: storage is no longer necessary
        # case 0011: storage is still necessary
        case0010 = np.logical_and(
            case001,
            pow_st < 0
        )
        case0011 = np.logical_and(
            case001,
            pow_st >= 0
        )

        # 0010: calculate charge power
        pow_c = (pow_im+pow_dp)-pow_ld

        # case 00100: storage is not fully charged
        # case 00101: storage is fully charged
        case00100 = np.logical_and(
            case0010,
            np.logical_not(self.st.is_full)
        )
        case00101 = np.logical_and(
            case0010,
            self.st.is_full
        )

        # case 001010: sink does not absorb all the power
        # case 001011: sink absorbs all the power
        case001010 = np.logical_and(
            case00101,
            pow_skmax < pow_c
        )
        case001011 = np.logical_and(
            case00101,
            pow_skmax >= pow_c
        )

        # 001010: determine power for net metering
        gdc001010 = case001010*(pow_c-pow_skmax)
        sk001010 = case001010*pow_skmax

        # 001011: give power to sink
        sk001011 = case001011*pow_c

        # case 001000: not beyond max charge
        # case 001001: beyond max charge
        case001000 = np.logical_and(
            case00100,
            pow_c <= pow_maxc
        )
        case001001 = np.logical_and(
            case00100,
            pow_c > pow_maxc
        )

        # 001000: determine power for charging
        stc001000 = case001000*pow_c

        # 001001: max charge then give excess to sink
        stc001001 = case001001*pow_maxc

        # case 0010010: sink does not absorb all the power
        # case 0010011: sink absorbs all the power
        case0010010 = np.logical_and(
            case001001,
            pow_skmax < pow_c-pow_maxc
        )
        case0010011 = np.logical_and(
            case001001,
            pow_skmax >= pow_c-pow_maxc
        )

        # 0010010: determine power for net metering
        gdc0010010 = case0010010*(pow_c-pow_maxc-pow_skmax)
        sk0010010 = case0010010*pow_skmax

        # 0010011: give power to sink
        sk0010011 = case0010011*(pow_c-pow_maxc)

        # 0011: adjust storage output
        std0011 = case0011*pow_st

        # collect total powers
        stc_tot = np.maximum(
            (  # charge storage
                stc100+stc101+stc001000+stc001001
            ),
            0
        )
        std_tot = np.maximum(
            (  # discharge storage
                std01+std000+std0011
            ),
            0
        )
        dp_tot = np.maximum(
            (  # run dispatchables
                dp00
            ),
            0
        )
        sk_tot = np.maximum(
            (  # net metering to grid
                sk111+sk1011+sk001011+sk0010011 +
                sk110+sk1010+sk001010+sk0010010
            ),
            0
        )
        gdc_tot = np.maximum(
            (  # net metering to grid
                gdc110+gdc1010+gdc001010+gdc0010010
            ),
            0
        )
        gdd_tot = np.maximum(
            (  # take power from grid
                gdd000
            ),
            0
        )

        out = (
            pow_im, stc_tot, std_tot, dp_tot,
            sk_tot, gdc_tot, gdd_tot
        )

        return out

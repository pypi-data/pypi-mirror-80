# test on synchrotron module
import numpy as np
import astropy.units as u
from astropy.constants import e, c, m_e
from agnpy.emission_regions import Blob
import pytest


mec2 = m_e.to("erg", equivalencies=u.mass_energy())
# a global test blob with spectral index 2
SPECTRUM_NORM = 1e-13 * u.Unit("cm-3")
GAMMA_MIN = 1
GAMMA_B = 100
GAMMA_MAX = 1e6
PWL_IDX_2_DICT = {
    "type": "PowerLaw",
    "parameters": {"p": 2.0, "gamma_min": GAMMA_MIN, "gamma_max": GAMMA_MAX},
}
BPL_DICT = {
    "type": "BrokenPowerLaw",
    "parameters": {
        "p1": 2.4,
        "p2": 3.4,
        "gamma_b": GAMMA_B,
        "gamma_min": GAMMA_MIN,
        "gamma_max": GAMMA_MAX,
    },
}
# blob parameters
R_B = 1e16 * u.cm
Z = 0.1
DELTA_D = 10
GAMMA = 10
B = 0.1 * u.G
PWL_BLOB = Blob(R_B, Z, DELTA_D, GAMMA, B, SPECTRUM_NORM, PWL_IDX_2_DICT)
BPL_BLOB = Blob(R_B, Z, DELTA_D, GAMMA, B, SPECTRUM_NORM, BPL_DICT)
# useful for checks
BETA = 1 - 1 / np.power(GAMMA, 2)
V_B = 4 / 3 * np.pi * np.power(R_B, 3)

class TestSynchrotron:
    """class grouping all tests related to the Synchrotron class"""


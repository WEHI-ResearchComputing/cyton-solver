"""
Last Edit: 11-Feb-2024

Cyton2 Algorithm Model
"""

from cyton.core.types import *
from cyton.core.models import ExtrapolationResults

class Cyton2Model:
    t0: float
    tf: float
    dt: float
    times: ExtrapolationTimes
    nt: int
    n0: float
    ht: PerTime[HarvestTime]
    nreps: NReps
    exp_max_div: MaxGeneration
    max_div: MaxGeneration
    logn: bool

    def __init__(
        self,
        ht: PerTime[HarvestTime],
        n0: float,
        max_div: MaxGeneration,
        dt: float,
        nreps: NReps = [],
        logn: bool = True,
    ):
        ...

    def compute_pdf(self, times: ExtrapolationTimes, mu: float, sig: float) -> NDArray[np.float_]:
        ...

    def compute_cdf(self, times: ExtrapolationTimes, mu: float, sig: float) -> NDArray[np.float_]:
        ...

    def compute_sf(self, times: ExtrapolationTimes, mu: float, sig: float) -> NDArray[np.float_]:
        ...

    # # Return sum of dividing and destiny cells in each generation
    # def evaluate(
    #     self, params: Parameters
    # ) -> NDArray[np.float_]:
    #     ...

    def evaluate(self,
        mUns: float, sUns: float,
        mDiv0: float, sDiv0: float,
        mDD: float, sDD: float,
        mDie: float, sDie: float,
        b: float, DTYPE_t: float
    ) -> NDArray[np.float_]:
        ...

    def extrapolate(
        self, model_times: ExtrapolationTimes, params: Parameters
    ) -> ExtrapolationResults:
        ...

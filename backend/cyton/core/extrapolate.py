from cyton.core.settings import DEFAULT_EXP_HT, DEFAULT_MAX_DIV, DEFAULT_N0, DT
from cyton.core.types import HarvestTime, PerTime, ExtrapolationTimes, ExtrapolationResults, Parameters
import numpy as np
from cyton.core.model import Cyton2Model

def get_times(exp_ht: PerTime[HarvestTime]) -> ExtrapolationTimes:
    """
    Convert from harvest times to extrapolation times
    """
    t0 = 0
    tf = max(exp_ht) + 5
    return np.linspace(t0, tf, num=int(tf/DT)+1)

def extrapolate_without_data(params: Parameters) -> ExtrapolationResults:
    """
    Perform an extrapolation using only model parameters, but no data
    """
    return Cyton2Model(
        ht=DEFAULT_EXP_HT,
        n0 = DEFAULT_N0,
        max_div = DEFAULT_MAX_DIV,
        dt = DT
    ).extrapolate(model_times = get_times(DEFAULT_EXP_HT), params=params)

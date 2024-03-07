"""
Last Edit: 21-Feb-2024

Function for Endpoint: Extrapolate
"""
from cyton.core.model_fitting import get_times, extrapolate
from cyton.core.settings import DT
from cyton.core import types
from cyton.core.cyton2 import Cyton2Model

def extrapolate_model(exp_ht: types.HarvestTimes, max_div: types.MaxGeneration, params: types.Parameters) -> types.ExtrapolatedData:
    """
    Extrapolate and predict the model's behavior.

    Params:
        exp_ht: Experimental metadata
        max_div_per_conditions: Experimental metadata
        params: Fitted parameters

    Returns:
    - dict: A dictionary containing extrapolated data
    """
    times = get_times(exp_ht)
    n0 = calc_n0(nreps[0])
    model = Cyton2Model(exp_ht, n0, max_div, DT)
    results = extrapolate(model, times, params)
    
    # Convert the NumPy arrays to regular lists to allow serializing to JSON
    return {
            "ext_total_live_cells": results["ext_total_live_cells"].tolist(),
            "ext_cells_per_gen": results["ext_cells_per_gen"].tolist(),
            "hts_total_live_cells": results["hts_total_live_cells"].tolist(),
            "hts_cells_per_gen": results["hts_cells_per_gen"]
            }
    

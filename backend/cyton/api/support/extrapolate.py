"""
Last Edit: 21-Feb-2024

Function for Endpoint: Extrapolate
"""
from cyton.core.model_fitting import get_times, extrapolate
from cyton.core.settings import N0, DT
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
    # nreps is not needed for extrapolation
    model = Cyton2Model(exp_ht, N0, max_div, DT)
    ext_total_live_cells, ext_cells_per_gen, hts_total_live_cells, hts_cells_per_gen = extrapolate(model, times, params)
    
    # Convert the NumPy arrays to regular lists to allow serializing to JSON
    return {
            "ext_total_live_cells": ext_total_live_cells.tolist(),
            "ext_cells_per_gen": ext_cells_per_gen.tolist(),
            "hts_total_live_cells": hts_total_live_cells.tolist(),
            "hts_cells_per_gen": hts_cells_per_gen
            }
    

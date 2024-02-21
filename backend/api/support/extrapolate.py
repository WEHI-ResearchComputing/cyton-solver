"""
Last Edit: 21-Feb-2024

Function for Endpoint: Extrapolation

Returns the extrapolated data as a dictionary
"""
from core.model_fitting import get_model, get_times, extrapolate
from core.settings import N0, DT
from core.settings import DEFAULT_EXP_HT, DEFAULT_CELL_GENS_REPS, DEFAULT_MAX_DIV_PER_CONDITIONS

def extract_experiment_data(data):
    return data.get('exp_ht'), data.get('cell_gens_reps'), data.get('max_div_per_conditions')

def get_default_experiment_data():
    return [DEFAULT_EXP_HT], [DEFAULT_CELL_GENS_REPS], [DEFAULT_MAX_DIV_PER_CONDITIONS]

def extrapolate_model(exp_ht, max_div_per_conditions, nreps, params):
    times = get_times(exp_ht)
    model = get_model(exp_ht, N0, max_div_per_conditions, DT, nreps)
    ext_total_live_cells, ext_cells_per_gen, hts_total_live_cells, hts_cells_per_gen = extrapolate(model, times, params)
    
    # Convert the NumPy arrays to regular lists to allow serializing to JSON
    extrapolated_data = {
            "ext_total_live_cells": ext_total_live_cells.tolist(),
            "ext_cells_per_gen": ext_cells_per_gen.tolist(),
            "hts_total_live_cells": hts_total_live_cells.tolist(),
            "hts_cells_per_gen": hts_cells_per_gen
            }
    
    return extrapolated_data

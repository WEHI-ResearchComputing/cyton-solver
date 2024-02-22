"""
Last Edit: 11-Feb-2024

Function for Endpoint: Start Fit

Returns the fitted parameters
"""
import pandas as pd
from core.model_fitting import get_parameters, get_model, fit
from core.settings import DEFAULT_PARS, DEFAULT_BOUNDS, DEFAULT_VARY, N0, DT

def extract_experiment_data(data):
    return data.get('exp_ht'), data.get('cell_gens_reps'), data.get('max_div_per_conditions')
 
def fit_model(exp_ht, cell_gens_reps, max_div_per_conditions):
    
    nreps = [len(l) for l in cell_gens_reps[0]]
    # TODO: 
    params, paramExcl = get_parameters(DEFAULT_PARS, DEFAULT_BOUNDS, DEFAULT_VARY)
    model = get_model(exp_ht, N0, max_div_per_conditions, DT, nreps)

    return fit(exp_ht, cell_gens_reps, params, paramExcl, model)

def start_background_fit(exp_ht, cell_gens_reps, max_div_per_conditions, task_id):

    mUns, sUns, mDiv0, sDiv0, mDD, sDD, mDie, sDie, b, p = fit_model(exp_ht, cell_gens_reps, max_div_per_conditions)
    fitted_parameters = {
        'mUns': mUns,
        'sUns': sUns,
        'mDiv0': mDiv0,
        'sDiv0': sDiv0,
        'mDD': mDD,
        'sDD': sDD,
        'mDie': mDie,
        'sDie': sDie,
        'b': b,
        'p': p
    }
    
    # Save the fitted parameters to a CSV file
    df = pd.DataFrame.from_dict(fitted_parameters, orient='index').transpose()
    df.to_csv(f'fitted_parameters_{task_id}.csv', index=False)
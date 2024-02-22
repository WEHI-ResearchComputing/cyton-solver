"""
Last Edit: 11-Feb-2024

Function for Endpoint: Start Fit
"""
import pandas as pd
from core.model_fitting import get_parameters, get_model, fit
from core.settings import N0, DT

def extract_experiment_data(data):
    return data.get('exp_ht'), data.get('cell_gens_reps'), data.get('max_div_per_conditions')

def extract_settings(settings):
    """
    Extract parameter settings, bounds, and vary.

    Parameters:
    - settings: Dictionary containing parameter, bounds, and vary settings.

    Returns:
    - parameters: Dictionary containing parameter values.
    - bounds: Dictionary containing lower and upper bounds.
    - vary: Dictionary containing boolean values indicating whether parameters vary.
    """
    return settings.get("parameters"), settings.get("bounds"), settings.get("vary")

def fit_model(exp_ht, cell_gens_reps, max_div_per_conditions, settings):
    """
    Perform model fitting with the provided experiment data and settings.

    Parameters:
    - exp_ht
    - cell_gens_reps
    - max_div_per_conditions
    - settings: Dictionary containing parameter, bounds, and vary settings.

    Returns:
    - Fitted model parameters
    """
    nreps = [len(l) for l in cell_gens_reps[0]]
    parameters, bounds, vary = extract_settings(settings)
    params, paramExcl = get_parameters(parameters, bounds, vary)
    model = get_model(exp_ht, N0, max_div_per_conditions, DT, nreps)

    return fit(exp_ht, cell_gens_reps, params, paramExcl, model)

def start_background_fit(exp_ht, cell_gens_reps, max_div_per_conditions, settings, task_id):
    """
    Start a background fitting job and save the fitted parameters to a CSV file when completed.

    Parameters:
    - exp_ht
    - cell_gens_reps
    - max_div_per_conditions
    - task_id: Unique identifier for the fitting task
    """

    # Fit the model and get the fitted parameters
    mUns, sUns, mDiv0, sDiv0, mDD, sDD, mDie, sDie, b, p = fit_model(exp_ht, cell_gens_reps, max_div_per_conditions, settings)

    # Save the fitted parameters to a dictionary
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
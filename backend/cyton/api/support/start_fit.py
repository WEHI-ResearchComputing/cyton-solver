"""
Last Edit: 11-Feb-2024

Function for Endpoint: Start Fit
"""
import pandas as pd
from cyton.core.model_fitting import get_parameters, fit
from cyton.core.settings import N0, DT
from cyton.core import types
from cyton.core.cyton2 import Cyton2Model

def extract_settings(settings: types.ExperimentSettings):
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

def fit_model(exp_ht: types.HarvestTimes, cell_gens_reps: types.CellPerGensReps, max_div_per_conditions: types.MaxGeneration, settings: types.ExperimentSettings) -> types.Parameters:
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
    params, paramExcl = get_parameters(settings["parameters"], settings["bounds"], settings["vary"])
    n0 = calc_n0(cell_gens_reps[0])
    model = Cyton2Model(exp_ht, n0, max_div_per_conditions, DT, nreps)

    return fit(exp_ht, cell_gens_reps, params, paramExcl, model)

def start_background_fit(exp_ht: types.HarvestTimes, cell_gens_reps: types.CellPerGensReps, max_div_per_conditions: types.MaxGeneration, settings: types.ExperimentSettings, task_id: str) -> None:
    """
    Start a background fitting job and save the fitted parameters to a CSV file when completed.

    Parameters:
    - exp_ht
    - cell_gens_reps
    - max_div_per_conditions
    - task_id: Unique identifier for the fitting task
    """

    # Fit the model and get the fitted parameters
    fitted_parameters = fit_model(exp_ht, cell_gens_reps, max_div_per_conditions, settings)
    
    # Save the fitted parameters to a CSV file
    # See discussion here: https://github.com/python/mypy/issues/4976 on why this type error occurs.
    df = pd.DataFrame.from_dict(fitted_parameters, orient='index').transpose() # type: ignore
    df.to_csv(f'fitted_parameters_{task_id}.csv', index=False)

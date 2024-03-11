"""
Last Edit: 11-Feb-2024

Function for Endpoint: Start Fit
"""
import pandas as pd
from cyton.core.types import *
from cyton.core.models import ExperimentSettings, SingleConditionData

def start_background_fit(data: SingleConditionData, settings: ExperimentSettings, task_id: str) -> None:
    """
    Start a background fitting job and save the fitted parameters to a CSV file when completed.
    """

    # Fit the model and get the fitted parameters
    model = data.get_model()
    fitted_parameters = data.fit_model(model, settings)
    
    # Save the fitted parameters to a CSV file
    # See discussion here: https://github.com/python/mypy/issues/4976 on why this type error occurs.
    df = pd.DataFrame.from_dict(fitted_parameters, orient='index').transpose() # type: ignore
    df.to_csv(f'fitted_parameters_{task_id}.csv', index=False)

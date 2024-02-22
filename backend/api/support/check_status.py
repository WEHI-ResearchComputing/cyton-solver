"""
Last Edit: 21-Feb-2024

Function for Endpoint: Check Status
"""
import os
import pandas as pd

def get_fitted_parameters(task_id):
    """
    Retrieve fitted parameters from a CSV file associated with a given task ID.

    Parameters:
    - task_id: The unique identifier for the fitting task.

    Returns:
    - fitted_parameters: A dictionary containing the fitted parameters, or None if the file does 
      not exist/ has not been completed.
    """

    # Check if the fitted parameters file exists
    file_path = f'fitted_parameters_{task_id}.csv'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
        # Convert the fitted parameters to a dictionary
            fitted_parameters = pd.read_csv(file_path).to_dict(orient='records')[0]
        # Deletes the file
        os.remove(file_path)

    else:
        # If the file does not exist, return None
        fitted_parameters = None

    return fitted_parameters
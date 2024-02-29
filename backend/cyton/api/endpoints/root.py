import os, tempfile, uuid
from typing import Optional
from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException, Request
from cyton.api.support.logger import initialize_logger
from cyton.api.support.upload import parse_file
from cyton.api.support.extrapolate import extract_experiment_data, get_default_experiment_data, extrapolate_model
from cyton.api.support.start_fit import start_background_fit
from cyton.api.support.default_settings import get_default_settings
from cyton.api.support.check_status import get_fitted_parameters
from cyton.core.types import DefaultSettings

router = APIRouter()
log = initialize_logger()

# =======================
# Default Settings Endpoint:
# =======================
@router.get("/default_settings")
async def default_settings(request: Request) -> DefaultSettings:
    """
    Returns a dictionary with the default settings (parameters, bounds, vary).

    Parameters:
    - request: The FastAPI Request object representing the incoming HTTP request.

    Returns:
    - dict: A dictionary containing the default settings.
    """
    log.info(f"/default_settings was accessed from: {request.client}. Returning default settings.")

    try:
        default_settings = get_default_settings()
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to get default settings. Please try again.")
    
    log.info("Default settings returned successfully.")

    return default_settings

# =======================
# Upload Endpoint:
# =======================
@router.post('/upload')
async def upload(request: Request, file: UploadFile = File(...)):
    """
    Returns a dictionary with the extracted experimental data from the file to the client

    Parameters:
    - request: The FastAPI Request object representing the incoming HTTP request.
    - file: The file to be uploaded. Expected in the request's form data.

    Returns:
    - dict: A dictionary containing the experiment data parsed from the uploaded file.
    """
    log.info("/upload was accessed from: " + str(request.client))

    try:
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
            # Write the contents to a temporary file
            temp_file.write(contents)
            temp_file_path = temp_file.name

        # Parse the file and extract the data
        experiment_data = parse_file(temp_file_path)
        
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to upload file. Please try again.")
    
    finally:
        if temp_file_path:
            os.remove(temp_file_path)
        log.info("Upload successful. Returning experiment data.")

    return {"experiment_data": experiment_data}

# =======================
# Model Extrapolation Endpoint:
# =======================
@router.post('/extrapolate')
async def extrapolate(request: Request, parameters: dict, data: Optional[dict] = None):
    """
    Returns the extrapolated data as a dictionary. 
    Parameters dictionary must be provided, and experiment data is optional.

    Parameters:
    - request: The FastAPI Request object representing the incoming HTTP request.
    - parameters: Dictionary of parameters.
    - data: Optional dictionary containing experiment data.

    Returns:
    - dict: A dictionary containing the extrapolated data.
    """
    log.info("/extrapolate was accessed from: " + str(request.client))

    try:
        if data:
            # If experiment data is provided, extract the data
            exp_ht, cell_gens_reps, max_div_per_conditions = extract_experiment_data(data)
        else:
            # If no experiment data is provided, use defaults
            exp_ht, cell_gens_reps, max_div_per_conditions = get_default_experiment_data()

        extrapolated_data = extrapolate_model(exp_ht, max_div_per_conditions, cell_gens_reps, parameters)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to extrapolate model. Please try again.")

    log.info("Model extrapolation successful. Returning extrapolated data.")

    return {"extrapolated_data": extrapolated_data}

# =======================
# Start Fit Endpoint
# =======================
@router.post('/start_fit')
async def start_fit(request: Request, data: dict, settings:dict, background_tasks: BackgroundTasks):
    """
    Initiates a background fitting job and returns a taskID to the client.

    Parameters:
    - request: The FastAPI Request object representing the incoming HTTP request.
    - data: Dictionary containing experiment data.
    - settings: Dictionary containing the fitting settings (parameters, bounds, vary).
    - background_tasks: FastAPI class for scheduling background tasks.

    Returns:
    - task_id: A dictionary containing the taskID.
    """
    log.info("/start_fit was accessed from: " + str(request.client))

    try:
        # Extract the experiment data
        exp_ht, cell_gens_reps, max_div_per_conditions = extract_experiment_data(data['experiment_data'])

        # Generate a unique taskID
        task_id = str(uuid.uuid4())

        # Start the fitting job in the background
        background_tasks.add_task(start_background_fit, exp_ht, cell_gens_reps, max_div_per_conditions, settings, task_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to start fit. Please try again.")
    
    log.info("Fitting job started successfully." + " Task ID: " + task_id)

    return {"task_id": task_id}

# =======================
# Check Status Endpoint
# =======================
@router.post('/check_status')
async def check_status(request: Request, data: dict):
        """
        Checks the status of a fitting job and returns the fitted parameters if completed.
        Else, returns None.

        Parameters:
        - request: The FastAPI Request object representing the incoming HTTP request.
        - data: Dictionary containing task_id for checking the status.

        Returns:
        - dict: A dictionary containing the fitted parameters.
        """
        log.info("/check_status was accessed from: " + str(request.client))

        if not data.get('task_id'):
            raise HTTPException(status_code=400, detail="task_id is required.")
        
        task_id = data.get('task_id')

        try:
            # Returns None if the task is not completed
            fitted_parameters = get_fitted_parameters(task_id)
    
        except Exception as e:
            raise HTTPException(status_code=400, detail="Failed to check status. Please try again.")
    
        log.info("Status checked successfully for task ID: " + task_id)
    
        return {"fitted_parameters_" + task_id : fitted_parameters}

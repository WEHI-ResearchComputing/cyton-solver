import os, tempfile, uuid
from typing import Optional
from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException, Request
from api.support.logger import initialize_logger
from api.support.upload import parse_file
from api.support.extrapolate import extract_experiment_data, get_default_experiment_data, extrapolate_model
from api.support.start_fit import start_background_fit
from api.support.default_parameters import get_default_parameters
from api.support.check_status import get_fitted_parameters

router = APIRouter()
log = initialize_logger()

# =======================
# Default Parameters Endpoint:
#
# Returns a dictionary with the default parameters
# =======================
@router.get("/default_parameters")
async def default_parameters(request: Request):

    log.info("/default_parameters was accessed from: " + str(request.client) + ". Returning default parameters.")

    try:
        default_parameters = get_default_parameters()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to get default parameters. Please try again.")
    
    log.info("Default parameters returned successfully.")

    return default_parameters

# =======================
# File Upload Endpoint:
#
# Returns a dictionary with the extracted data from the file to the client
# =======================
@router.post('/upload')
async def upload(request: Request, file: UploadFile = File(...)):

    log.info("/upload was accessed from: " + str(request.client))

    try:
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
            # Write the contents to a temporary file
            temp_file.write(contents)
            temp_file_path = temp_file.name

        # Parse the file and extract the data
        experiment_data = parse_file(temp_file_path)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to upload file. Please try again.")
    
    finally:
        if temp_file_path:
            os.remove(temp_file_path)
        log.info("Upload successful. Returning experiment data.")

    return {"experiment_data": experiment_data}

# =======================
# Model Extrapolation Endpoint:
#
# Returns the extrapolated data as a dictionary
# Parameters dictionary must be provided, and experiment data is optional
# =======================
@router.post('/extrapolate')
async def extrapolate(request: Request, parameters: dict, data: Optional[dict] = None):

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
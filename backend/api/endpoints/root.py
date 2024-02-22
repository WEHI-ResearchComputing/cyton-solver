import os, tempfile, uuid
from typing import Optional, Dict
from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException
from api.support.upload import parse_file
from api.support.extrapolate import extract_experiment_data, get_default_experiment_data, extrapolate_model
from api.support.start_fit import start_background_fit
from api.support.default_parameters import get_default_parameters
router = APIRouter()

# =======================
# Default Parameters Endpoint:
#
# Returns a dictionary with the default parameters
# =======================
@router.get("/default_parameters")
async def default_parameters():
    return get_default_parameters()

# =======================
# File Upload Endpoint:
#
# Returns a dictionary with the extracted data from the file to the client
# =======================
@router.post('/upload')
async def upload(file: UploadFile = File(...)):
    
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

    return {"experiment_data": experiment_data}

# =======================
# Model Extrapolation Endpoint:
#
# Returns the extrapolated data as a dictionary
# Parameters dictionary must be provided, and experiment data is optional
# =======================
@router.post('/extrapolate')
async def extrapolate(parameters: dict, data: Optional[dict] = None):

    if data:
        # If experiment data is provided, extract the data
        exp_ht, cell_gens_reps, max_div_per_conditions = extract_experiment_data(data)

    else:
        # If no experiment data is provided, use defaults
        exp_ht, cell_gens_reps, max_div_per_conditions = get_default_experiment_data()

    extrapolated_data = extrapolate_model(exp_ht, max_div_per_conditions, cell_gens_reps, parameters)

    return {"extrapolated_data": extrapolated_data}
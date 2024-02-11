from http.client import HTTPException
import os, tempfile, copy
from fastapi import APIRouter, File, UploadFile
from backend.core.file_reader import ReadData
from backend.core.data_manager import compute_total_cells, sort_cell_generations
from backend.core.utils import create_check_matrix

router = APIRouter()

@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    
    try:
        contents = await file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
            temp_file.write(contents)
            temp_file_path = temp_file.name
    
        data_reader = ReadData(temp_file_path)
        exp_ht = data_reader.harvested_times
        exp_ht_reps = data_reader.harvested_times_reps
        max_div_per_conditions = data_reader.generation_per_condition
        conditions = data_reader.condition_names
        exp_num_tp = data_reader.num_time_points
        
        total_cells, total_cells_reps, total_cells_sem = compute_total_cells(
            data_reader.data,
            data_reader.condition_names,
            data_reader.num_time_points,
            data_reader.generation_per_condition
        )

        cell_gens, cell_gens_reps, cell_gens_sem = sort_cell_generations(
            data_reader.data,
            data_reader.condition_names,
            data_reader.num_time_points,
            data_reader.generation_per_condition
        )

        c15_check = create_check_matrix(copy.deepcopy(cell_gens_reps))

        data = {
                "exp_ht": exp_ht,
                "exp_ht_reps": exp_ht_reps,
                "max_div_per_conditions": max_div_per_conditions,
                "conditions": conditions,
                "exp_num_tp": exp_num_tp,
                "total_cells": total_cells,
                "total_cells_reps": total_cells_reps,
                "total_cells_sem": total_cells_sem,
                "cell_gens": cell_gens,
                "cell_gens_reps": cell_gens_reps,
                "cell_gens_sem": cell_gens_sem,
                "c15_check": c15_check
            }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to upload file. Please try again.")
    
    finally:
        if temp_file_path:
            os.remove(temp_file_path)

    return {"data": data}
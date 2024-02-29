"""
Last Edit: 21-Feb-2024

Function for Endpoint: Upload
"""
import copy
from cyton.core.file_reader import ReadData
from cyton.core.data_manager import compute_total_cells, sort_cell_generations
from cyton.core.utils import create_check_matrix
from cyton.core import types

def parse_file(temp_file_path: str) -> types.ExperimentData:
    """
    Parse data from a file and return a dictionary containing the extracted experiment data.

    Parameters:
    - temp_file_path: The path to the temporary file

    Returns:
    - dict: A dictionary containing experiment data extracted from the file.
    """
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

    data: types.ExperimentData = {
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
    
    return data

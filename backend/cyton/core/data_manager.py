"""
Last Edit: 11-Feb-2024

Reshape an input data format to a 4D array (icnd, itpt, igen, irep)
"""
from scipy.stats import sem
from cyton.core.utils import remove_empty
from cyton.core.types import *

def compute_total_cells(data: PerCond[PerTime[PerRep[PerGen[CellCount | None]]]], conditions: Conditions, num_tps: NumTimePoints, gen_per_condition: PerCond[MaxGeneration]) -> tuple[
	PerCond[PerTime[CellTotal]], PerCond[Reps[CellTotal]], PerCond[PerTime[CellTotalSem]]
]:
	"""
	All parameters are output of file_reader.py object, which consists meta information about the data itself.

	:param data: number of cells per generation (4-dimensional array) = data[icnd][itpt][irep][igen]
	:param conditions: names of condition
	:param num_tps: number of time points per condition
	:param gen_per_condition: number of maximum generations per condition
	:return: [average total cells, total cells with replicates, standard error of means]
	"""
	
	num_conditions = len(conditions)

	# Computation of average total cells
	max_length = 0
	total_cells = [[] for _ in range(num_conditions)]
	for icnd in range(num_conditions):
		for itpt in range(num_tps[icnd]):
			cell = 0.
			for igen in range(gen_per_condition[icnd]+1):
				temp = 0.
				replicate = 0.
				size_of_data = len(data[icnd][itpt][igen])
				# Check for single replicate and update
				if size_of_data == 0:
					replicate = 1.
				# Loop through replicates
				for datum in data[icnd][itpt][igen]:
					if datum is not None:
						temp += datum
						replicate += 1
					# Finds maximum number of replicates in the experiment (useful for asymmetric data)
					if max_length < size_of_data:
						max_length = size_of_data
				temp = temp / replicate
				cell += temp
			total_cells[icnd].append(cell)
	filtered_total_cells = remove_empty(total_cells)

	# Computation of total cells for each replicates
	total_cells_reps = [[] for _ in range(num_conditions)]
	total_cells_reps2 = [[[] for _ in range(max(num_tps))] for _ in range(num_conditions)]
	for icnd in range(num_conditions):
		for itpt in range(num_tps[icnd]):
			tmp = [0. for _ in range(max_length)]
			for igen in range(gen_per_condition[icnd]+1):
				for irep, datum in enumerate(data[icnd][itpt][igen]):
					if not isinstance(datum, (int, float)):
						raise Exception(f"Unknown data {datum} in condition {icnd}, timepoint {itpt} and generation {igen}")
					tmp[irep] += datum
			for idx in range(len(data[icnd][itpt][gen_per_condition[icnd]])):
				total_cells_reps[icnd].append(tmp[idx])
				total_cells_reps2[icnd][itpt].append(tmp[idx])
	filtered_total_cells_reps = remove_empty(total_cells_reps)
	filtered_total_cells_reps2 = remove_empty(total_cells_reps2)

	# Computation of standard error of mean for replicates
	total_cells_sem = [[] for _ in range(num_conditions)]
	for icnd in range(num_conditions):
		for itpt in range(num_tps[icnd]):
			total_cells_sem[icnd].append(sem(filtered_total_cells_reps2[icnd][itpt]))
	filtered_total_cells_sem = remove_empty(total_cells_sem)

	return filtered_total_cells, filtered_total_cells_reps, filtered_total_cells_sem

def sort_cell_generations(data: PerCond[PerTime[PerRep[PerGen[CellCount | None]]]], conditions: Conditions, num_tps: NumTimePoints, gen_per_condition: PerCond[MaxGeneration]) -> tuple[
	PerCond[PerTime[PerGen[CellAverage]]], PerCond[PerTime[PerRep[PerGen[CellCount]]]], PerCond[PerTime[PerGen[CellTotalSem]]]
]:
	"""
	This function organises cell-generation profile.

	:param data: (nested list) number of cells per generation (4-dimensional array) = data[icnd][itpt][irep][igen]
	:param conditions: (list) names of condition
	:param num_tps: (list) number of time points per condition
	:param gen_per_condition: (list) number of maximum generations per condition
	:return: (tuple) [average cell per gen, cell per gen with replicates, standard error of means]
	"""
	
	num_conditions = len(conditions)

	# Computation of average cell numbers : dynamically determines replicates
	max_length = 0
	cell_gens = [[] for _ in range(num_conditions)]
	for icnd in range(num_conditions):
		for itpt in range(num_tps[icnd]):
			gen_arr = []
			for igen in range(gen_per_condition[icnd]+1):
				cell = 0.
				replicate = 0.
				size_of_data = len(data[icnd][itpt][igen])
				if size_of_data == 0:
					replicate = 1.
				for datum in data[icnd][itpt][igen]:
					if datum is not None:
						cell += datum
						replicate += 1.
					if max_length < size_of_data:
						max_length = size_of_data
				cell = cell / replicate
				gen_arr.append(cell)
			cell_gens[icnd].append(gen_arr)
			
	filtered_cell_gens = remove_empty(cell_gens)

	cell_gens_reps = [[[] for _ in range(max(num_tps))] for _ in range(num_conditions)]
	for icnd in range(num_conditions):
		for itpt in range(num_tps[icnd]):
			tmp = [[] for _ in range(max_length)]
			for igen in range(gen_per_condition[icnd]+1):
				for irep, datum in enumerate(data[icnd][itpt][igen]):
					tmp[irep].append(datum)
			for idx in range(len(data[icnd][itpt][gen_per_condition[icnd]])):
				cell_gens_reps[icnd][itpt].append(tmp[idx])

	filtered_cell_gens_reps = remove_empty(cell_gens_reps)

	# Re-sort filtered dataset to compute SEM : schema - [icnd][itpt][igen][irep]
	resorted_data = [
		[
			[
				[] for _ in range(max(gen_per_condition)+1)
			] for _ in range(max(num_tps))
		] for _ in range(num_conditions)
	]
	cell_gens_sem = [
		[] for _ in range(num_conditions)
	]
	for icnd in range(len(filtered_cell_gens_reps)):
		for itpt in range(len(filtered_cell_gens_reps[icnd])):
			for irep, l in enumerate(filtered_cell_gens_reps[icnd][itpt]):
				for igen, datum in enumerate(l):
					resorted_data[icnd][itpt][igen].append(datum)
			tmp = []
			for idx in range(len(resorted_data[icnd][itpt])):
				tmp.append(sem(resorted_data[icnd][itpt][idx]))
			cell_gens_sem[icnd].append(tmp)

	filtered_cell_gens_sem = remove_empty(cell_gens_sem)

	return filtered_cell_gens, filtered_cell_gens_reps, filtered_cell_gens_sem

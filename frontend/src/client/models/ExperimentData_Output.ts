/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Conditions } from './Conditions';
import type { PerCond_int_ } from './PerCond_int_';
import type { PerCond_MaxGeneration_ } from './PerCond_MaxGeneration_';
import type { PerCond_PerTime_CellTotal___Output } from './PerCond_PerTime_CellTotal___Output';
import type { PerCond_PerTime_CellTotalSem___Output } from './PerCond_PerTime_CellTotalSem___Output';
import type { PerCond_PerTime_HarvestTime___Output } from './PerCond_PerTime_HarvestTime___Output';
import type { PerCond_PerTime_PerGen_CellAverage____Output } from './PerCond_PerTime_PerGen_CellAverage____Output';
import type { PerCond_PerTime_PerGen_CellTotalSem____Output } from './PerCond_PerTime_PerGen_CellTotalSem____Output';
import type { PerCond_PerTime_PerRep_PerGen_CellCount_____Output } from './PerCond_PerTime_PerRep_PerGen_CellCount_____Output';
import type { PerCond_Reps_CellTotal___Output } from './PerCond_Reps_CellTotal___Output';
import type { PerCond_Reps_HarvestTime___Output } from './PerCond_Reps_HarvestTime___Output';

/**
 * Experiment data for all conditions
 */
export type ExperimentData_Output = {
    exp_ht: PerCond_PerTime_HarvestTime___Output;
    exp_ht_reps: PerCond_Reps_HarvestTime___Output;
    max_div_per_conditions: PerCond_MaxGeneration_;
    conditions: Conditions;
    exp_num_tp: PerCond_int_;
    total_cells: PerCond_PerTime_CellTotal___Output;
    total_cells_reps: PerCond_Reps_CellTotal___Output;
    total_cells_sem: PerCond_PerTime_CellTotalSem___Output;
    cell_gens: PerCond_PerTime_PerGen_CellAverage____Output;
    cell_gens_reps: PerCond_PerTime_PerRep_PerGen_CellCount_____Output;
    cell_gens_sem: PerCond_PerTime_PerGen_CellTotalSem____Output;
};


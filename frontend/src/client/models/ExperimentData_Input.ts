/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Conditions } from './Conditions';
import type { PerCond_int_ } from './PerCond_int_';
import type { PerCond_MaxGeneration_ } from './PerCond_MaxGeneration_';
import type { PerCond_PerTime_CellTotal___Input } from './PerCond_PerTime_CellTotal___Input';
import type { PerCond_PerTime_CellTotalSem___Input } from './PerCond_PerTime_CellTotalSem___Input';
import type { PerCond_PerTime_HarvestTime___Input } from './PerCond_PerTime_HarvestTime___Input';
import type { PerCond_PerTime_PerGen_CellAverage____Input } from './PerCond_PerTime_PerGen_CellAverage____Input';
import type { PerCond_PerTime_PerGen_CellTotalSem____Input } from './PerCond_PerTime_PerGen_CellTotalSem____Input';
import type { PerCond_PerTime_PerRep_PerGen_CellCount_____Input } from './PerCond_PerTime_PerRep_PerGen_CellCount_____Input';
import type { PerCond_Reps_CellTotal___Input } from './PerCond_Reps_CellTotal___Input';
import type { PerCond_Reps_HarvestTime___Input } from './PerCond_Reps_HarvestTime___Input';

/**
 * Experiment data for all conditions
 */
export type ExperimentData_Input = {
    exp_ht: PerCond_PerTime_HarvestTime___Input;
    exp_ht_reps: PerCond_Reps_HarvestTime___Input;
    max_div_per_conditions: PerCond_MaxGeneration_;
    conditions: Conditions;
    exp_num_tp: PerCond_int_;
    total_cells: PerCond_PerTime_CellTotal___Input;
    total_cells_reps: PerCond_Reps_CellTotal___Input;
    total_cells_sem: PerCond_PerTime_CellTotalSem___Input;
    cell_gens: PerCond_PerTime_PerGen_CellAverage____Input;
    cell_gens_reps: PerCond_PerTime_PerRep_PerGen_CellCount_____Input;
    cell_gens_sem: PerCond_PerTime_PerGen_CellTotalSem____Input;
};


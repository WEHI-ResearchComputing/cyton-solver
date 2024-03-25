/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { np_ndarray } from './np_ndarray';
import type { PerGen_PerTime_float__ } from './PerGen_PerTime_float__';
import type { PerTime_HarvestTime_ } from './PerTime_HarvestTime_';
import type { tuple_int_np_dtype_float64 } from './tuple_int_np_dtype_float64';

export type HarvestTimeResults = {
    harvest_times: PerTime_HarvestTime_;
    total_live_cells: np_ndarray;
    cells_gen: PerGen_PerTime_float__;
};


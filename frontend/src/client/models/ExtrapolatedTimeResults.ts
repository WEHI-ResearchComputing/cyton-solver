/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ExtrapolationTimes } from './ExtrapolationTimes';
import type { np_ndarray } from './np_ndarray';
import type { tuple_int_int_np_dtype_float64 } from './tuple_int_int_np_dtype_float64';
import type { tuple_int_np_dtype_float64 } from './tuple_int_np_dtype_float64';

export type ExtrapolatedTimeResults = {
    time_points: ExtrapolationTimes;
    total_live_cells: np_ndarray;
    cells_gen: np_ndarray;
    nUNS: np_ndarray;
    nDIV: np_ndarray;
    nDES: np_ndarray;
};


/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Bounds } from './Bounds';
import type { FittableParams } from './FittableParams';
import type { Parameters } from './Parameters';

/**
 * Settings that define how the model will be fitted
 */
export type ExperimentSettings_Input = {
    parameters: Parameters;
    bounds: Bounds;
    vary: FittableParams;
};


/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_extrapolate_extrapolate_post } from '../models/Body_extrapolate_extrapolate_post';
import type { Body_start_fit_start_fit_post } from '../models/Body_start_fit_start_fit_post';
import type { Body_upload_upload_post } from '../models/Body_upload_upload_post';
import type { ExperimentData_Output } from '../models/ExperimentData_Output';
import type { ExperimentSettings_Output } from '../models/ExperimentSettings_Output';
import type { ExtrapolationResults } from '../models/ExtrapolationResults';
import type { Parameters } from '../models/Parameters';
import type { TaskId } from '../models/TaskId';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class RootService {

    /**
     * Default Settings
     * Returns a dictionary with the default settings (parameters, bounds, vary).
     *
     * Parameters:
     * - request: The FastAPI Request object representing the incoming HTTP request.
     *
     * Returns:
     * - dict: A dictionary containing the default settings.
     * @returns ExperimentSettings_Output Successful Response
     * @throws ApiError
     */
    public static defaultSettingsDefaultSettingsGet(): CancelablePromise<ExperimentSettings_Output> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/default_settings',
        });
    }

    /**
     * Upload
     * Returns a dictionary with the extracted experimental data from the file to the client
     *
     * Parameters:
     * - request: The FastAPI Request object representing the incoming HTTP request.
     * - file: The file to be uploaded. Expected in the request's form data.
     *
     * Returns:
     * - dict: A dictionary containing the experiment data parsed from the uploaded file.
     * @returns ExperimentData_Output Successful Response
     * @throws ApiError
     */
    public static uploadUploadPost({
        formData,
    }: {
        formData: Body_upload_upload_post,
    }): CancelablePromise<ExperimentData_Output> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/upload',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Extrapolate
     * Returns the extrapolated data as a dictionary.
     * Parameters dictionary must be provided, and experiment data is optional.
     *
     * Parameters:
     * - request: The FastAPI Request object representing the incoming HTTP request.
     * - parameters: Dictionary of parameters.
     * - data: Optional dictionary containing experiment data.
     *
     * Returns:
     * - dict: A dictionary containing the extrapolated data.
     * @returns ExtrapolationResults Successful Response
     * @throws ApiError
     */
    public static extrapolateExtrapolatePost({
        requestBody,
        condition,
    }: {
        requestBody: Body_extrapolate_extrapolate_post,
        condition?: (string | null),
    }): CancelablePromise<ExtrapolationResults> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/extrapolate',
            query: {
                'condition': condition,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Start Fit
     * Initiates a background fitting job and returns a taskID to the client.
     *
     * Parameters:
     * - request: The FastAPI Request object representing the incoming HTTP request.
     * - data: Dictionary containing experiment data.
     * - settings: Dictionary containing the fitting settings (parameters, bounds, vary).
     * - background_tasks: FastAPI class for scheduling background tasks.
     *
     * Returns:
     * - task_id: A dictionary containing the taskID.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static startFitStartFitPost({
        condition,
        requestBody,
    }: {
        condition: string,
        requestBody: Body_start_fit_start_fit_post,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/start_fit',
            query: {
                'condition': condition,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Check Status
     * Checks the status of a fitting job and returns the fitted parameters if completed.
     * Else, returns None.
     *
     * Parameters:
     * - request: The FastAPI Request object representing the incoming HTTP request.
     * - data: Dictionary containing task_id for checking the status.
     *
     * Returns:
     * - dict: A dictionary containing the fitted parameters.
     * @returns Parameters Successful Response
     * @throws ApiError
     */
    public static checkStatusCheckStatusPost({
        taskId,
    }: {
        taskId: TaskId,
    }): CancelablePromise<Parameters> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/check_status',
            query: {
                'task_id': taskId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}

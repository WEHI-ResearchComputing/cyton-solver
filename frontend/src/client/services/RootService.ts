/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_extrapolate_api_extrapolate_post } from '../models/Body_extrapolate_api_extrapolate_post';
import type { Body_start_fit_api_start_fit_post } from '../models/Body_start_fit_api_start_fit_post';
import type { Body_upload_api_upload_post } from '../models/Body_upload_api_upload_post';
import type { ExperimentData_Output } from '../models/ExperimentData_Output';
import type { ExperimentSettings_Output } from '../models/ExperimentSettings_Output';
import type { ExtrapolationResults } from '../models/ExtrapolationResults';
import type { Parameters } from '../models/Parameters';
import type { TaskId } from '../models/TaskId';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class RootService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

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
    public defaultSettingsApiDefaultSettingsGet(): CancelablePromise<ExperimentSettings_Output> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/default_settings',
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
    public uploadApiUploadPost({
        formData,
    }: {
        formData: Body_upload_api_upload_post,
    }): CancelablePromise<ExperimentData_Output> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/upload',
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
    public extrapolateApiExtrapolatePost({
        requestBody,
        condition,
    }: {
        requestBody: Body_extrapolate_api_extrapolate_post,
        condition?: (string | null),
    }): CancelablePromise<ExtrapolationResults> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/extrapolate',
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
    public startFitApiStartFitPost({
        condition,
        requestBody,
    }: {
        condition: string,
        requestBody: Body_start_fit_api_start_fit_post,
    }): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/start_fit',
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
    public checkStatusApiCheckStatusPost({
        taskId,
    }: {
        taskId: TaskId,
    }): CancelablePromise<Parameters> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/check_status',
            query: {
                'task_id': taskId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}

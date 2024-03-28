import { ApiError } from "./client";

export function makeErrorMsg(error: Error): string {
    if (error instanceof ApiError) {
        return `Error processing file: ${error.statusText}. ${error.body.detail}`;
    }
    else {
        return `Error processing file: ${error}`;
    }
}

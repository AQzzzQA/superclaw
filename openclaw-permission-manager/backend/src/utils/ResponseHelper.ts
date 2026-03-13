export interface SuccessResponse<T = any> {
  success: true;
  data: T;
  message?: string;
}

export interface ErrorResponse {
  success: false;
  error: string;
  details?: any;
}

export class ResponseHelper {
  static success<T = any>(data: T, message?: string): SuccessResponse<T> {
    return {
      success: true,
      data,
      message
    };
  }

  static error(error: string, details?: any): ErrorResponse {
    return {
      success: false,
      error,
      details
    };
  }
}
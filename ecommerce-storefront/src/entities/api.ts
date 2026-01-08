export type ActionResponse<T> = {
  success: boolean;
  data?: T;
  error?: string;
  unauthorized?: boolean;
  validationErrors?: Record<string, string>; // For FastAPI validation errors
  status?: number;
};

export type BackendValidationError = {
  msg: string;
  loc: string[];
  type: string;
};

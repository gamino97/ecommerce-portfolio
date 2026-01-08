import { cookies } from 'next/headers';
import { ActionResponse, BackendValidationError } from '@/entities/api';

export const API_URL = process.env.API_URL;

export async function getHeaders() {
  const cookieStore = await cookies();
  const token = cookieStore.get('access_token')?.value;
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

export async function fetchApi(path: string, options: RequestInit = {}) {
  const headers = await getHeaders();
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      ...headers,
      ...options.headers,
    },
  });
  return res;
}

export async function handleRequest<T>(
  response: Response
): Promise<ActionResponse<T>> {
  const data = await response.json();

  if (response.ok) {
    return { success: true, data, status: response.status };
  }
  if (response.status === 403) {
    return { success: false, unauthorized: true, status: response.status };
  }

  if (response.status === 422) {
    // Mapeo de errores de FastAPI (loc, msg) a React Hook Form
    const validationErrors: Record<string, string> = {};
    data.detail.forEach((err: BackendValidationError) => {
      const field = err.loc[err.loc.length - 1];
      validationErrors[field] = err.msg;
    });
    return { success: false, validationErrors, status: response.status };
  }

  return {
    success: false,
    error: data.detail || 'Something went wrong',
    status: response.status
  };
}

import { cookies } from 'next/headers';

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

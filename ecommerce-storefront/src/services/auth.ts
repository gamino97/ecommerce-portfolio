import { LoginData, RegisterData } from '@/entities/user';

const API_URL = process.env.API_URL;

export async function login(data: LoginData) {
  const params = new URLSearchParams();
  params.append('username', data.email);
  params.append('password', data.password);

  const response = await fetch(`${API_URL}/auth/jwt/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: params,
  });

  if (!response.ok) {
    const error = await response.json();
    console.error(error);
    throw new Error(error.detail || 'Login failed');
  }

  return response.json();
}

export async function register(data: RegisterData) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Registration failed');
  }

  return response.json();
}

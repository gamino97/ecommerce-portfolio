import { LoginData, LoginResponse, RegisterData, User } from '@/entities/user';
import { fetchApi, handleRequest } from './api';

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
  return await handleRequest<LoginResponse>(response);
}

export async function register(data: RegisterData) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return await handleRequest<User>(response);
}

export async function get_me() {
  const response = await fetchApi('/users/me');
  return await handleRequest<User>(response);
}

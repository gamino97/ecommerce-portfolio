'use server';

import { cookies } from 'next/headers';
import { get_me, login, register } from '@/services/auth';
import { z } from 'zod';
import { registerSchema } from '@/entities/user';
import { redirect, notFound } from 'next/navigation';

const loginSchema = z.object({
  email: z.email('Invalid email address'),
  password: z.string().min(1, 'Password is required'),
});

export async function loginAction(prevState: unknown, formData: FormData) {
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;
  const validatedFields = loginSchema.safeParse({ email, password });
  if (!validatedFields.success) {
    return { error: 'Invalid fields' };
  }
  const response = await login({ email, password });
  if (!response.success || !response.data) {
    if (response.error === 'LOGIN_BAD_CREDENTIALS') {
      return { error: 'Invalid email or password' };
    }
    return { error: 'Something went wrong' };
  }

  // Store token in HttpOnly cookie
  const cookieStore = await cookies();
  cookieStore.set('access_token', response.data.access_token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    path: '/',
    maxAge: 3600, // 1 hour
  });
  return { success: true };
}

export async function registerAction(formData: FormData) {
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;
  const first_name = formData.get('first_name') as string;
  const last_name = formData.get('last_name') as string;

  const validatedFields = registerSchema.safeParse({
    email,
    password,
    first_name,
    last_name,
  });

  if (!validatedFields.success) {
    return { error: 'Invalid fields' };
  }

  const response = await register({
    email,
    password,
    first_name,
    last_name,
  });

  if (!response.success) {
    if (response.error === 'REGISTER_USER_ALREADY_EXISTS') {
      return { error: 'User with this email already exists' };
    }
    return { error: response.error || 'Something went wrong' };
  }

  // Automatically login after registration
  const loginResponse = await login({ email, password });
  if (loginResponse.success && loginResponse.data) {
    const cookieStore = await cookies();
    cookieStore.set('access_token', loginResponse.data.access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      path: '/',
      maxAge: 3600, // 1 hour
    });
    return { success: true };
  }

  return { success: true, message: 'Registration successful. Please login.' };
}

export async function logoutAction() {
  const cookieStore = await cookies();
  cookieStore.delete('access_token');
}

export async function get_user_action() {
  const response = await get_me();
  if (!response.success) {
    return null;
  }
  return response.data;
}

export async function get_super_user_action() {
  const response = await get_me();
  if (!response.success) {
    return null;
  }
  const user = response.data;
  if (!user) {
    redirect('/login');
  }
  if (!user.is_superuser) {
    notFound();
  }
}

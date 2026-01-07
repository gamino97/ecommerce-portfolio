'use server';

import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { get_me, login } from '@/services/auth';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.email(),
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

'use server';

import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { login } from '@/services/auth';
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

  try {
    const { access_token } = await login({ email, password });

    // Store token in HttpOnly cookie
    const cookieStore = await cookies();
    cookieStore.set('access_token', access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      path: '/',
      maxAge: 3600, // 1 hour
    });

  } catch (error) {
    if (error instanceof Error) {
      return { error: error.message };
    }
    return { error: 'An unexpected error occurred' };
  }
  return { success: true };

}

export async function logoutAction() {
  const cookieStore = await cookies();
  cookieStore.delete('access_token');
  redirect('/login');
}

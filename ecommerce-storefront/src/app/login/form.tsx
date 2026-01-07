'use client';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { loginAction } from '@/actions/auth';
import { LoginFormValues, loginSchema } from './utils';
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/components/ui/form';
import { useActionState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

// Define the state type based on the action return type
type LoginState = { error?: string, success?: boolean } | null;

export default function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirect = searchParams.get('redirect');
  const [state, formAction, isPending] = useActionState<LoginState, FormData>(
    loginAction,
    null
  );
  const form = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const {
    setError
  } = form;

  useEffect(() => {
    if (state?.error) {
      setError('root', { message: state.error });
    } else if (state?.success) {
      router.push(redirect || '/dashboard');
    }
  }, [state, setError, redirect, router]);

  return (
    <Form {...form}>
      <form className="space-y-4" action={formAction}>
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="Enter your email" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input type="password" placeholder="Enter your password" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        {form.formState.errors.root && (
          <div className="text-red-500 text-sm">
            {form.formState.errors.root.message}
          </div>
        )}
        <Button type="submit" className="w-full" disabled={isPending}>
          {isPending ? 'Signing in...' : 'Sign In'}
        </Button>
      </form>
    </Form>
  );
}

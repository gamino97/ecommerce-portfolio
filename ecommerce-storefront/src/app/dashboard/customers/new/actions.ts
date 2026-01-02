'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { schema, CustomerValidator } from '@/entities/customer';
import { fetchApi } from '@/services/api';

type ActionState = {
  errors: Record<string, { message: string }>;
};

async function createCustomer(data: CustomerValidator): Promise<ActionState> {
  const { error: parseError } = schema.safeParse(data);
  const errors: ActionState['errors'] = {};
  for (const { path, message } of parseError?.issues || []) {
    errors[path.join('.')] = { message };
  }
  if (Object.keys(errors).length > 0) {
    return {
      errors,
    };
  }

  const values = {
    first_name: data.firstName,
    last_name: data.lastName,
  };

  const response = await fetchApi('/customers', {
    method: 'POST',
    body: JSON.stringify(values),
  });

  if (!response.ok) {
    const errorData = await response.json();
    return {
      errors: {
        firstName: { message: errorData.detail || 'Failed to create customer' },
      },
    };
  }

  revalidatePath('/dashboard/customers', 'layout');
  redirect('/dashboard/customers');
}

export {
  createCustomer,
};

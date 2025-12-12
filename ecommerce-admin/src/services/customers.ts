import { fetchApi } from './api';
import { type Customer } from '@/entities/customer';

export async function getCustomers(): Promise<Customer[]> {
  const response = await fetchApi('/customers/');
  if (!response.ok) throw new Error('Failed to fetch customers');
  return response.json();
}

export function getFullName(user: Partial<Customer>) {
  return `${user.first_name || ''} ${user.last_name || ''}`;
}

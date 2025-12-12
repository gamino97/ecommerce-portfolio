import { fetchApi } from './api';

export type Category = {
  id: string;
  name: string;
};

export async function getCategories(): Promise<Category[]> {
  const response = await fetchApi('/categories');
  if (!response.ok) throw new Error('Failed to fetch categories');
  return response.json();
}

// End of file

import { fetchApi } from './api';
import { Product, ProductInsert } from '@/entities/product';

export async function getProducts(): Promise<Product[]> {
  const response = await fetchApi('/products');
  if (!response.ok) throw new Error('Failed to fetch products');
  return response.json();
}

export async function getProductById(id: string): Promise<Product | null> {
  const response = await fetchApi(`/products/${id}`);
  if (!response.ok) {
    if (response.status === 404) return null;
    throw new Error('Failed to fetch product');
  }
  const product = await response.json();
  return product;
}

export async function createProduct(product: ProductInsert) {
  const response = await fetchApi('/products', {
    method: 'POST',
    body: JSON.stringify(product),
  });
  if (!response.ok) throw new Error('Failed to create product');
  return response.json();
}

export async function updateProduct(
  id: string,
  updates: Partial<ProductInsert>
) {

  const response = await fetchApi(`/products/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(updates),
  });
  if (!response.ok) throw new Error('Failed to update product');
  return await response.json();
}

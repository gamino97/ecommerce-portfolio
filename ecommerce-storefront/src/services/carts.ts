import { fetchApi } from './api';

export interface Cart {
  id: number;
  user_id: string | null;
  items: Record<string, number>;
}

export async function createCart(): Promise<number> {
  const res = await fetchApi('/carts', {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to create cart');
  // The backend returns the ID as a string in the response body
  const cartId = await res.json();
  return parseInt(cartId);
}

export async function getCart(cartId: number): Promise<Cart> {
  const res = await fetchApi(`/carts/${cartId}`);
  if (!res.ok) throw new Error('Failed to fetch cart');
  return res.json();
}

export async function updateCart(
  cartId: number,
  items: Record<string, number>
): Promise<Cart> {
  const res = await fetchApi(`/carts/${cartId}`, {
    method: 'PUT',
    body: JSON.stringify({ items }),
  });
  if (!res.ok) throw new Error('Failed to update cart');
  return res.json();
}

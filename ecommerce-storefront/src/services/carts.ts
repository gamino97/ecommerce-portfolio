import { fetchApi } from './api';

interface StoreError {
  message: string;
}

export interface CartItem {
  product_id: string;
  name: string;
  description: string;
  image_url: string;
  quantity: number;
  price: number;
  line_total: number;
  stock: number;
}

export interface CartSummary {
  subtotal: string;
  grand_total: string;
  total_items_count: number;
}

export interface Cart {
  id: number;
  user_id: string | null;
  items: CartItem[];
  summary: CartSummary;
  updated_at: string;
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

export async function addItemToCart(
  cartId: number,
  productId: string,
  quantity: number
): Promise<Cart | StoreError> {
  const res = await fetchApi(`/carts/${cartId}/items/`, {
    method: 'POST',
    body: JSON.stringify({ product_id: productId, quantity }),
  });
  if (!res.ok) {
    const error = await res.json();
    console.log(error);
    if (res.status === 400 || res.status === 404) {
      return { message: error.detail };
    }
    return { message: 'Failed to add item to cart' };
  }
  return await res.json();
}

export async function updateItemInCart(
  cartId: number,
  productId: string,
  quantity: number
): Promise<Cart> {
  const res = await fetchApi(`/carts/${cartId}/items/${productId}`, {
    method: 'PUT',
    body: JSON.stringify({ quantity }),
  });
  if (!res.ok) throw new Error('Failed to update item in cart');
  return res.json();
}

export async function removeItemFromCart(
  cartId: number,
  productId: string
): Promise<Cart> {
  const res = await fetchApi(`/carts/${cartId}/items/${productId}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Failed to remove item from cart');
  return res.json();
}

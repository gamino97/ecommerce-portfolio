'use server';

import { cookies } from 'next/headers';
import { revalidatePath } from 'next/cache';
import { createCart, getCart, updateCart } from '@/services/carts';

const CART_ID_COOKIE = 'nexstore_cart_id';

export async function getCartAction() {
  const cookieStore = await cookies();
  const cartIdStr = cookieStore.get(CART_ID_COOKIE)?.value;

  if (!cartIdStr) return null;

  try {
    return await getCart(parseInt(cartIdStr));
  } catch (error) {
    console.error('Failed to get cart:', error);
    return null;
  }
}

export async function addToCartAction(productId: string, quantity: number = 1) {
  const cookieStore = await cookies();
  const cartIdStr = cookieStore.get(CART_ID_COOKIE)?.value;
  let cartId: number;

  if (!cartIdStr) {
    cartId = await createCart();
    cookieStore.set(CART_ID_COOKIE, cartId.toString(), {
      path: '/',
      httpOnly: true,
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 7, // 1 week
    });
  } else {
    cartId = parseInt(cartIdStr);
  }

  const cart = await getCart(cartId);
  const currentItems = cart.items || {};
  const newItems = {
    ...currentItems,
    [productId]: (currentItems[productId] || 0) + quantity,
  };

  await updateCart(cartId, newItems);

  revalidatePath('/', 'layout');
}

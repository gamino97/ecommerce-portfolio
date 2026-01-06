'use server';

import { cookies } from 'next/headers';
import { revalidatePath } from 'next/cache';
import {
  addItemToCart,
  createCart,
  getCart,
  removeItemFromCart,
  updateItemInCart,
} from '@/services/carts';

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
  const result = await addItemToCart(cartId, productId, quantity);
  revalidatePath('/', 'layout');
  return result;
}

export async function updateCartQuantityAction(
  productId: string,
  quantity: number
) {
  const cookieStore = await cookies();
  const cartIdStr = cookieStore.get(CART_ID_COOKIE)?.value;
  if (!cartIdStr) return;
  const cartId = parseInt(cartIdStr);
  if (quantity <= 0) {
    await removeItemFromCart(cartId, productId);
  } else {
    await updateItemInCart(cartId, productId, quantity);
  }
  revalidatePath('/', 'layout');
}

export async function removeFromCartAction(productId: string) {
  const cookieStore = await cookies();
  const cartIdStr = cookieStore.get(CART_ID_COOKIE)?.value;
  if (!cartIdStr) return;
  const cartId = parseInt(cartIdStr);
  await removeItemFromCart(cartId, productId);
  revalidatePath('/', 'layout');
}

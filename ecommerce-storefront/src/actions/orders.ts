'use server';

import { createOrder } from '@/services/orders';
import { redirect } from 'next/navigation';
import { z } from 'zod';
import { cookies } from 'next/headers';
import { CART_ID_COOKIE } from '@/entities/cart';
import { Order } from '@/entities/order';
import { ActionResponse } from '@/entities/api';

const checkoutSchema = z.object({
  shipping_address: z.string().min(5, 'Address is too short').max(200),
  cart_id: z.string().transform((val) => parseInt(val)),
});

export async function createOrderAction(
  prevState: unknown,
  formData: FormData
): Promise<ActionResponse<Order>> {
  const shipping_address = formData.get('shipping_address') as string;
  const cart_id = formData.get('cart_id') as string;
  const validatedFields = checkoutSchema.safeParse({
    shipping_address,
    cart_id,
  });
  if (!validatedFields.success) {
    return {
      success: false,
      error: 'Invalid fields'
    };
  }
  const result = await createOrder(
    validatedFields.data.cart_id,
    validatedFields.data.shipping_address
  );
  if (!result.success) {
    if (result.unauthorized) {
      redirect('/login');
    }
    return result;
  }
  const cookieStore = await cookies();
  cookieStore.delete(CART_ID_COOKIE);
  redirect(`/store/orders/${result.data?.id}`);
}

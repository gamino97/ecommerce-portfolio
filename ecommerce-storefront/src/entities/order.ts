import { z } from 'zod';
import { Product } from '@/entities/product';

export const orderStatuses = [
  'pending',
  'shipped',
  'canceled',
] as const;

export type OrderStatus = typeof orderStatuses[number];

export const orderItemSchema = z.object({
  id: z.string().optional(),
  product_id: z.uuid({ message: 'Product is required' }),
  quantity: z.number({ message: 'Quantity is required' }).int().positive({ message: 'Quantity must be at least 1' }),
});

export type OrderItem = z.infer<typeof orderItemSchema> & {
  price: number, subtotal: string, product: Product,
};

export const orderSchema = z.object({
  customerId: z.string({ message: 'Customer is required' }),
  status: z.enum(orderStatuses, {
    message: 'Status is required',
  }),
  items: z
    .array(orderItemSchema)
    .min(1, 'At least one item is required'),
});

export type OrderUser = {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
};

export type Order = {
  id: number;
  status: string;
  shipping_address: string;
  created_at: string;
  total_price: string;
  user: OrderUser;
  order_items: OrderItem[];
};

export const checkoutSchema = z.object({
  shipping_address: z
    .string()
    .min(5, 'Address is too short')
    .max(200, 'Address is too long'),
});

export type CheckoutValues = z.infer<typeof checkoutSchema>;

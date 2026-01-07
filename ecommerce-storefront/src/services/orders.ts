'use server';

import { fetchApi, handleRequest } from './api';
import { type Order } from '@/entities/order';

export async function getOrders(): Promise<Order[]> {
  const response = await fetchApi('/orders/');
  if (!response.ok) throw new Error('Failed to fetch orders');
  return response.json();
}

export async function getOrder(id: string): Promise<Order | null> {
  const response = await fetchApi(`/orders/${id}`);
  if (!response.ok) return null;
  return await response.json();
}

export async function countOrders(): Promise<number> {
  const response = await fetchApi('/orders/count');
  if (!response.ok) return 0;
  const data = await response.json();
  return data.count;
}

export async function getTotalSalesPrice(): Promise<number> {
  const response = await fetchApi('/orders/total-sales');
  if (!response.ok) return 0;
  const data = await response.json();
  return data.total_sales;
}

export async function getLowStockItems(): Promise<number> {
  const response = await fetchApi('/products/low-stock/count');
  if (!response.ok) return 0;
  const data = await response.json();
  return data.count;
}

// Reuse getCustomers from customers service or fetch here
export async function getCustomers() {
  return getCustomersCount();
}

export async function getCustomersCount(): Promise<number> {
  const response = await fetchApi('/customers/count');
  if (!response.ok) return 0;
  const data = await response.json();
  return data.count;
}

export async function createOrder(
  cartId: number,
  shippingAddress: string
) {
  const response = await fetchApi(`/carts/${cartId}/orders/`, {
    method: 'POST',
    body: JSON.stringify({ shipping_address: shippingAddress }),
  });
  return await handleRequest<Order>(response);
}

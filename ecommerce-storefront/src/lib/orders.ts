import Decimal from 'decimal.js';
import { type Order } from '@/entities/order';

export function getOrderTotalText({ order }: { order: Order }): string {
  let orderTotal = Decimal(order.total_price);
  if (orderTotal.isNaN()) orderTotal = Decimal(0);
  return Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(orderTotal.toNumber());
}

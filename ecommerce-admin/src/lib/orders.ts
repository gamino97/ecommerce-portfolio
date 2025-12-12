import Decimal from 'decimal.js';
import { Product } from '@/entities/product';
import { OrderItemPreview, type Order } from '@/entities/order';

export function getItemOrderSubtotal(
  { product, quantity }: { product: Product, quantity: number }) {
  return Decimal(product.price).mul(quantity);
}

export function getOrderTotal(
  { items, products = [] }: { items: OrderItemPreview[], products?: Product[] }
) {
  return items.reduce((total: Decimal, item) => {
    let product: Product | undefined;
    if (item.products) {
      product = item.products;
    } else {
      product = products.find(p => p.id === item.product_id);
    }
    if (!product) return total;
    return Decimal(total).add(getItemOrderSubtotal({
      product, quantity: item.quantity
    }));
  }, Decimal(0));
}

export function getOrderTotalText({ order }: { order: Order }): string {
  let orderTotal = Decimal(order.total_price);
  if (orderTotal.isNaN()) orderTotal = Decimal(0);
  return Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(orderTotal.toNumber());
}

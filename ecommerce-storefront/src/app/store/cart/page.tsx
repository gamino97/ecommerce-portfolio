import Link from 'next/link';
import { getCartAction } from '@/actions/cart';
import { CartItem } from '@/components/CartItem';
import { CartSummary } from '@/components/CartSummary';

export const metadata = {
  title: 'Shopping Cart',
  description: 'View and manage your shopping cart.',
};

function EmptyCart() {
  return (
    <div className="px-4 py-16 text-center">
      <h1 className="text-3xl font-bold mb-4">Your Cart is Empty</h1>
      <p className="text-muted-foreground mb-8">
        Looks like you haven&apos;t added anything to your cart yet.
      </p>
      <Link href="/store" className="text-primary hover:underline">
        Go back to shopping
      </Link>
    </div>
  );
}

export default async function CartPage() {
  const cart = await getCartAction();

  if (!cart || cart.items.length === 0) {
    return <EmptyCart />;
  }
  return (
    <div className="px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Shopping Cart</h1>
      <div className="grid lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-4">
          {cart.items.map((item) => (
            <CartItem key={item.product_id} item={item} />
          ))}
        </div>
        <div>
          <CartSummary
            subtotal={cart.summary.subtotal}
            total={cart.summary.grand_total}
            total_items_count={cart.summary.total_items_count}
          />
        </div>
      </div>
    </div>
  );
}

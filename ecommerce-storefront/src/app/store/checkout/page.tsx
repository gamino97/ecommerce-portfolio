import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { getCartAction } from '@/actions/cart';
import { Separator } from '@/components/ui/separator';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { CheckoutForm } from '@/app/store/checkout/CheckoutForm';

export const metadata = {
  title: 'Checkout',
  description: 'Checkout your order.',
};

export default async function CheckoutPage() {
  const cookieStore = await cookies();
  const token = cookieStore.get('access_token')?.value;

  if (!token) {
    redirect('/login?redirect=/store/checkout');
  }

  const cart = await getCartAction();

  if (!cart || cart.items.length === 0) {
    redirect('/store');
  }

  return (
    <div className="max-w-4xl mx-auto py-10">
      <h1 className="text-3xl font-bold mb-8">Checkout</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <Card>
            <CardHeader>
              <CardTitle>Shipping Address</CardTitle>
              <CardDescription>
                Enter where you&apos;d like your order to be delivered.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <CheckoutForm cartId={cart.id} />
            </CardContent>
          </Card>
        </div>
        <div>
          <Card>
            <CardHeader>
              <CardTitle>Order Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {cart.items.map((item) => (
                <div key={item.product_id} className="flex justify-between text-sm">
                  <span>{item.name} x {item.quantity}</span>
                  <span>${(item.price * item.quantity).toFixed(2)}</span>
                </div>
              ))}
              <Separator />
              <div className="flex justify-between font-medium">
                <span>Subtotal</span>
                <span>${cart.summary.subtotal}</span>
              </div>
              <div className="flex justify-between font-bold text-lg">
                <span>Total</span>
                <span>${cart.summary.grand_total}</span>
              </div>
            </CardContent>
            <CardFooter>
              <p className="text-xs text-muted-foreground">
                All prices include taxes and shipping.
              </p>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  );
}

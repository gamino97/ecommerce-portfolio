import { getOrder } from '@/services/orders';
import { notFound } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { ChevronLeft } from 'lucide-react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { formatPrice, getStatusColor } from '@/lib/utils';
import Image from 'next/image';
import { Metadata } from 'next';
interface Props {
  params: Promise<{ id: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { id } = await params;
  const order = await getOrder(id);
  if (!order) {
    return { title: 'Order not found' };
  }
  return {
    title: `Order #${order.id}`,
    description: `Order #${order.id}`,
  };
}

export default async function OrderDetailPage({ params }: Props) {
  const { id } = await params;
  const order = await getOrder(id);
  if (!order) {
    notFound();
  }

  return (
    <div className="max-w-3xl mx-auto py-10">
      <div className="mb-6">
        <Button variant="ghost" asChild className="pl-0 text-muted-foreground hover:text-foreground">
          <Link href="/store/orders" className="flex items-center gap-1">
            <ChevronLeft className="h-4 w-4" />
            My Orders
          </Link>
        </Button>
      </div>

      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Order #{order.id}</h1>
          <p className="text-muted-foreground">
            Placed on {new Date(order.created_at).toLocaleDateString()}
          </p>
        </div>
        <Badge className={getStatusColor(order.status)}>
          {order.status.toUpperCase()}
        </Badge>
      </div>

      <div className="grid grid-cols-1 gap-8">
        <Card>
          <CardHeader>
            <CardTitle>Items</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {order.order_items.map((item) => (
              <div key={item.id} className="flex justify-between items-center">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 rounded bg-muted flex items-center justify-center">
                    <Image
                      src={item.product.image_url}
                      alt={item.product.name}
                      width={48}
                      height={48}
                      unoptimized
                      className='h-12 w-12 object-cover'
                    />
                  </div>
                  <div>
                    <p className="font-medium">{item.product.name}</p>
                    <p className="text-sm text-muted-foreground">Qty: {item.quantity}</p>
                  </div>
                </div>
                <p className="font-medium">{formatPrice(item.subtotal)}</p>
              </div>
            ))}
            <Separator />
            <div className="flex justify-between font-bold text-lg pt-2">
              <span>Total Price</span>
              <span>{formatPrice(order.total_price)}</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Shipping Details</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <p className="text-sm font-medium text-muted-foreground">Address</p>
              <p>{order.shipping_address}</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

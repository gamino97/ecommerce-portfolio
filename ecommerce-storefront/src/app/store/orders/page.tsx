import { Order } from '@/entities/order';
import { ShoppingBag } from 'lucide-react';
import { getUserOrders } from '@/services/orders';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import Link from 'next/link';
import { redirect } from 'next/navigation';
import { formatPrice, getStatusColor } from '@/lib/utils';

function EmptyOrders() {
  return (
    <div className="flex flex-col items-center justify-center py-20 px-4 text-center">
      <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mb-4">
        <ShoppingBag className="w-8 h-8 text-muted-foreground" />
      </div>
      <h2 className="text-xl font-semibold">No orders found</h2>
      <p className="text-muted-foreground mt-2 max-w-xs">
        Looks like you haven&apos;t placed any orders yet.
        Start shopping to see your orders here!
      </p>
      <Button asChild className="mt-6">
        <Link href="/store">Browse Products</Link>
      </Button>
    </div>
  );
}

export default async function OrdersPage() {
  const { success, data: orders } = await getUserOrders();
  if (!success || !orders) redirect('/login');
  return (
    <div className="container mx-auto py-10 px-4 md:px-0">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">My Orders</h1>
          <p className="text-muted-foreground mt-1">
            Manage and view your order history.
          </p>
        </div>
      </div>
      <div className="rounded-xl border bg-card text-card-foreground shadow-sm overflow-hidden">
        {orders.length === 0 ? (
          <EmptyOrders />
        ) : (
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow className="hover:bg-transparent">
                  <TableHead className="w-[120px]">Order #</TableHead>
                  <TableHead>Date</TableHead>
                  <TableHead className="text-center">Items</TableHead>
                  <TableHead>Total</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {orders.map((order) => (
                  <TableRow key={order.id} className="group transition-colors">
                    <TableCell className="font-medium">
                      #{order.id}
                    </TableCell>
                    <TableCell>
                      {new Date(order.created_at).toLocaleDateString(
                        undefined,
                        {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric',
                        }
                      )}
                    </TableCell>
                    <TableCell className="text-center">
                      {order.order_items.reduce(
                        (acc, item) => acc + item.quantity,
                        0
                      )}
                    </TableCell>
                    <TableCell className="font-semibold">
                      {formatPrice(order.total_price)}
                    </TableCell>
                    <TableCell>
                      <Badge
                        variant="outline"
                        className={getStatusColor(order.status)}
                      >
                        {order.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="sm" asChild>
                        <Link href={`/store/orders/${order.id}`}>
                          View Details
                        </Link>
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </div>
    </div>
  );
}

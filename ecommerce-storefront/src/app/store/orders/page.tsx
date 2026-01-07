import { Order } from '@/entities/order';
import { getOrders } from '@/services/orders';
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
import { formatPrice } from '@/lib/utils';

function getStatusColor(status: string) {
  switch (status.toLowerCase()) {
    case 'pending':
      return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    case 'shipped':
      return 'bg-blue-100 text-blue-800 border-blue-200';
    case 'canceled':
      return 'bg-red-100 text-red-800 border-red-200';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-200';
  }
}

export default async function OrdersPage() {
  let orders: Order[] = [];
  try {
    orders = await getOrders();
  } catch {
    // In a real app, check if error is due to unauthorized and redirect
    // For now, if getOrders throws, we might want to redirect to login
    redirect('/login');
  }

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
          <div className="flex flex-col items-center justify-center py-20 px-4 text-center">
            <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mb-4">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="w-8 h-8 text-muted-foreground"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.11 4.63a3.375 3.375 0 0 1-3.356 4.183H6.142a3.375 3.375 0 0 1-3.356-4.183l1.11-4.63m15.356 0a3.375 3.375 0 0 0-3.356-4.183H6.142a3.375 3.375 0 0 0-3.356 4.183m15.356 0L15.75 10.5M8.25 10.5l1.11-4.63"
                />
              </svg>
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

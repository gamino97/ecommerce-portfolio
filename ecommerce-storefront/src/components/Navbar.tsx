import Link from 'next/link';
import { ShoppingBag, ShoppingCart, User as UserIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { getCartAction } from '@/actions/cart';
import { User } from '@/entities/user';

export async function Navbar({ user }: { user?: User | null }) {
  const cart = await getCartAction();
  const totalItems = cart?.summary.total_items_count || 0;
  return (
    <header className="border-b border-border/40 backdrop-blur-sm sticky top-0 z-50 bg-background/80">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/store" className="flex items-center gap-2 group">
          <div className="h-8 w-8 rounded-lg bg-primary/10 flex items-center justify-center transition-colors group-hover:bg-primary/20">
            <ShoppingBag className="w-5 h-5 text-primary" />
          </div>
          <span className="font-bold text-xl tracking-tight">NexStore</span>
        </Link>
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" asChild className="relative">
            <Link href="/store/cart">
              <ShoppingCart className="w-5 h-5" />
              {totalItems > 0 && (
                <Badge
                  className="absolute -top-1 -right-1 h-4 w-4 flex items-center justify-center p-0 text-[10px]"
                  variant="default"
                >
                  {totalItems}
                </Badge>
              )}
            </Link>
          </Button>
          <Button variant="ghost" size="icon" asChild>
            <Link href={user ? '/store/orders' : '/login'}>
              <UserIcon className="w-5 h-5" />
            </Link>
          </Button>
        </div>
      </div>
    </header>
  );
}

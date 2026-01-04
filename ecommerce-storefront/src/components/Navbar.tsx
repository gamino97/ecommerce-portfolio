import Link from 'next/link';
import { ShoppingBag, ShoppingCart, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { getCartAction } from '@/actions/cart';

export async function Navbar() {
  const cart = await getCartAction();
  console.log(cart);
  const totalItems = Object.values(cart?.items || {}).reduce(
    (acc: number, qty: unknown) => acc + (Number(qty) || 0),
    0
  );

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
            <Link href="/cart">
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
            <Link href="/login">
              <User className="w-5 h-5" />
            </Link>
          </Button>
        </div>
      </div>
    </header>
  );
}

'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Minus, Plus, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  updateCartQuantityAction,
  removeFromCartAction,
} from '@/actions/cart';
import { useTransition } from 'react';
import { formatPrice } from '@/lib/utils';
import { CartItem as CartItemType } from '@/services/carts';

interface CartItemProps {
  item: CartItemType;
}

export function CartItem({ item }: CartItemProps) {
  const [isPending, startTransition] = useTransition();

  const handle_update_quantity = (new_quantity: number) => {
    startTransition(async () => {
      await updateCartQuantityAction(item.product_id, new_quantity);
    });
  };

  const handle_remove = () => {
    startTransition(async () => {
      await removeFromCartAction(item.product_id);
    });
  };

  return (
    <div className="flex items-center space-x-4 py-4 border-b">
      <Link
        href={`/store/products/${item.product_id}`}
        className="flex items-center space-x-4 flex-1 min-w-0 hover:opacity-80 transition-opacity"
      >
        <div className="flex-shrink-0 relative w-24 h-24 rounded-md overflow-hidden bg-muted">
          <Image
            src={item.image_url}
            alt={item.name}
            fill
            className="object-cover"
            unoptimized
          />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-medium truncate">{item.name}</h3>
          <p className="mt-1 font-semibold">{formatPrice(item.price)}</p>
        </div>
      </Link>
      <div className="flex items-center space-x-2">
        <div className="flex items-center border rounded-md">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => handle_update_quantity(item.quantity - 1)}
            disabled={isPending || item.quantity <= 1}
            className="cursor-pointer"
          >
            <Minus className="h-4 w-4" />
          </Button>
          <span className="w-8 text-center">{item.quantity}</span>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => handle_update_quantity(item.quantity + 1)}
            disabled={isPending || item.quantity >= item.stock}
            className="cursor-pointer"
          >
            <Plus className="h-4 w-4" />
          </Button>
        </div>
        <Button
          variant="destructive"
          size="icon"
          onClick={handle_remove}
          disabled={isPending}
          className="cursor-pointer"
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}

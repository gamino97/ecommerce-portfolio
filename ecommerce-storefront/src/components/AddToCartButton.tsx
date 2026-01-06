'use client';

import { useTransition } from 'react';
import { ShoppingCart, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { addToCartAction } from '@/actions/cart';

interface AddToCartButtonProps {
  productId: string;
  disabled?: boolean;
}

export function AddToCartButton({ productId, disabled }: AddToCartButtonProps) {
  const [isPending, startTransition] = useTransition();

  const handleAddToCart = () => {
    startTransition(async () => {
      const result = await addToCartAction(productId);
      if ('message' in result) {
        toast.error(result.message);
      } else {
        toast.success('Added to cart');
      }
    });
  };

  return (
    <Button
      size="lg"
      className="w-full h-12 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300 active:scale-95 cursor-pointer"
      disabled={disabled || isPending}
      onClick={handleAddToCart}
    >
      {isPending ? (
        <Loader2 className="w-5 h-5 mr-2 animate-spin" />
      ) : (
        <ShoppingCart className="mr-2 h-5 w-5" />
      )}
      {disabled ? 'Out of Stock' : 'Add to Cart'}
    </Button>
  );
}

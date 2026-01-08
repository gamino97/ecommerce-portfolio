'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Product } from '@/entities/product';
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { cn, formatPrice } from '@/lib/utils';
import { AddToCartButton } from '@/components/AddToCartButton';

interface ProductCardProps {
  product: Product;
}

export function ProductCard({ product }: ProductCardProps) {
  return (
    <Card className="overflow-hidden hover:shadow-lg transition-all duration-300 group">
      <Link href={`/store/products/${product.id}`} className="flex flex-col flex-1">
        <CardHeader className="p-0">
          <div className="relative aspect-square overflow-hidden bg-muted">
            <Image
              src={product.image_url}
              alt={product.name}
              fill
              className="object-cover transition-transform group-hover:scale-105 duration-500"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
              unoptimized
            />
            <Badge className="absolute top-3 right-3 backdrop-blur-md bg-background/60 text-foreground border-none">
              {product.category.name}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="p-5 flex-1 flex flex-col">
          <CardTitle className="text-xl line-clamp-1 mb-2 group-hover:text-primary transition-colors">
            {product.name}
          </CardTitle>
          <p className="text-sm text-muted-foreground line-clamp-2 mb-4 flex-1">
            {product.description}
          </p>
          <div className="flex items-center justify-between mt-auto">
            <span className="text-2xl font-bold text-primary">
              {formatPrice(product.price)}
            </span>
            <span
              className={cn(
                'text-xs font-medium',
                product.stock === 0 ? 'text-destructive' : 'text-muted-foreground'
              )}
            >
              {product.stock === 0 ? 'Out of Stock' : `${product.stock} in stock`}
            </span>
          </div>
        </CardContent>
      </Link>
      <CardFooter className="p-4 pt-0">
        <AddToCartButton
          productId={product.id}
          disabled={product.stock === 0}
        />
      </CardFooter>
    </Card>
  );
}

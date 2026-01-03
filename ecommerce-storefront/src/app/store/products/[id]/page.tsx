import { notFound } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import { ChevronLeft, ShoppingCart, Package } from 'lucide-react';
import { getProductById } from '@/services/products';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { cn, formatPrice } from '@/lib/utils';

interface ProductPageProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function ProductDetailPage({ params }: ProductPageProps) {
  const { id } = await params;
  const product = await getProductById(id);

  if (!product) {
    notFound();
  }

  const is_out_of_stock = product.stock === 0;

  return (
    <div className="space-y-8">
      <Link
        href="/store"
        className="inline-flex items-center text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
      >
        <ChevronLeft className="mr-1 h-4 w-4" />
        Back to Catalog
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Product Image */}
        <div className="relative aspect-square overflow-hidden rounded-2xl bg-muted/30 border border-border/50">
          <Image
            src={product.image_url}
            alt={product.name}
            fill
            className="object-cover object-center transition-transform hover:scale-105 duration-500"
            sizes="(max-width: 768px) 100vw, 50vw"
            unoptimized
          />
          {is_out_of_stock && (
            <div className="absolute inset-0 bg-background/60 backdrop-blur-sm flex items-center justify-center">
              <Badge variant="destructive" className="px-4 py-1 text-base">Out of Stock</Badge>
            </div>
          )}
        </div>

        {/* Product Info */}
        <div className="flex flex-col space-y-6">
          <div className="space-y-2">
            <h1 className="text-4xl font-bold tracking-tight text-foreground">
              {product.name}
            </h1>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="font-medium">
                {product.category.name}
              </Badge>
              {product.stock > 0 && product.stock <= 5 && (
                <Badge variant="outline" className="text-amber-500 border-amber-500/50 bg-amber-500/5">
                  Only {product.stock} left in stock
                </Badge>
              )}
            </div>
          </div>

          <div className="text-3xl font-semibold text-primary">
            {formatPrice(product.price)}
          </div>

          <Separator className="bg-border/50" />

          <div className="space-y-4">
            <h3 className="text-lg font-medium">Description</h3>
            <p className="text-muted-foreground leading-relaxed">
              {product.description || 'No description available for this product.'}
            </p>
          </div>

          <Card className="bg-muted/30 border-border/50 overflow-hidden">
            <CardContent className="p-6 space-y-4">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Availability</span>
                <span className={cn('font-medium', is_out_of_stock ? 'text-destructive' : 'text-green-600')}>
                  {is_out_of_stock ? 'Out of Stock' : 'In Stock'}
                </span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Category</span>
                <span className="font-medium">{product.category.name}</span>
              </div>

              <Button
                size="lg"
                className="w-full h-12 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300"
                disabled={is_out_of_stock}
              >
                <ShoppingCart className="mr-2 h-5 w-5" />
                Add to Cart
              </Button>

            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

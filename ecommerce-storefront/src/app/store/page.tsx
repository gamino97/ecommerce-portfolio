import { getProducts } from '@/services/products';
import { ProductCard } from '@/components/ProductCard';

export default async function ProductsPage() {
  const products = await getProducts();

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">
          Featured Products
        </h1>
        <p className="text-muted-foreground">
          Explore our collection of high-quality products.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>

      {products.length === 0 && (
        <div className="text-center py-20 bg-muted/30 rounded-lg border-2 border-dashed border-border/50">
          <p className="text-muted-foreground">No products found.</p>
        </div>
      )}
    </div>
  );
}

'use client';

import { ProductInsert, Product } from '@/entities/product';
import { Category } from '@/services/categories';
import { ProductForm } from '@/components/product-form';
import { updateProductAction } from './actions';

interface EditProductFormProps {
  categories: Category[];
  product: Product;
}

export default function EditProductForm({
  categories,
  product,
}: EditProductFormProps) {
  async function handleSubmit(values: ProductInsert) {
    await updateProductAction(product.id, values);
  }
  return (
    <ProductForm
      categories={categories}
      initialValues={{
        name: product.name,
        description: product.description ?? '',
        image_url: product.image_url ?? '',
        price: Number(product.price),
        stock: Number(product.stock),
        category_id: product.category_id,
      }}
      onSubmit={handleSubmit}
    />
  );
}

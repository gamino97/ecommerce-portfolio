import { z } from 'zod';

export const categorySchema = z.object({
  id: z.uuid(),
  name: z.string().min(1),
});

export type Category = z.infer<typeof categorySchema>;

export const productSchema = z.object({
  id: z.uuid(),
  name: z.string().min(1, { message: 'Name is required' }),
  description: z.string().max(1000, { message: 'Description must be at most 1000 characters' }).optional(),
  image_url: z.url({ message: 'Image URL must be valid' }),
  price: z.number({ message: 'Price is required' }).positive({ message: 'Price must be positive' }),
  stock: z.number({ message: 'Stock is required' }).int().nonnegative({ message: 'Stock must be 0 or more' }),
  category_id: z.string({ message: 'Category is required' }),
  category: categorySchema,
});

// Schema for creating/updating (no id, no category)
export const productInsertSchema = productSchema.omit({
  id: true,
  category: true,
});

export type Product = z.infer<typeof productSchema>;
export type ProductInsert = z.infer<typeof productInsertSchema>;

export const defaultProductValues: ProductInsert = {
  name: '',
  description: '',
  image_url: '',
  price: 0,
  stock: 0,
  category_id: '',
};

import { z } from 'zod';
export const schema = z.object({
  id: z.string().optional(),
  firstName: z.string().min(1, 'First name is required'),
  lastName: z.string().min(1, 'Last name is required'),
});

export type CustomerValidator = z.infer<typeof schema>;

export type Customer = {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  created_at: string;
};

'use client';

import { useTransition } from 'react';
import { createOrderAction } from '@/actions/orders';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Loader2 } from 'lucide-react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { toast } from 'sonner';
import { checkoutSchema, CheckoutValues } from '@/entities/order';

interface Props {
  cartId: number;
}

export function CheckoutForm({ cartId }: Props) {
  const [isPending, startTransition] = useTransition();

  const form = useForm<CheckoutValues>({
    resolver: zodResolver(checkoutSchema),
    defaultValues: {
      shipping_address: '',
    },
  });

  async function onSubmit(data: CheckoutValues) {
    startTransition(async () => {
      const formData = new FormData();
      formData.append('shipping_address', data.shipping_address);
      formData.append('cart_id', cartId.toString());

      const result = await createOrderAction(null, formData);

      if (!result.success) {
        if ('validationErrors' in result && result.validationErrors) {
          Object.entries(result.validationErrors).forEach(([key, messages]) => {
            form.setError(key as keyof CheckoutValues, {
              type: 'server',
              message: messages[0],
            });
          });
        } else {
          toast.error(result.error);
        }
      }
    });
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="shipping_address"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Detailed Address</FormLabel>
              <FormControl>
                <Input
                  {...field}
                  placeholder="123 Street Name, City, Country"
                  disabled={isPending}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full cursor-pointer" disabled={isPending}>
          {isPending ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Processing...
            </>
          ) : (
            'Place Order'
          )}
        </Button>
      </form>
    </Form>
  );
}

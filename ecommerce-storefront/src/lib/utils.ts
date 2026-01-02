import { clsx, type ClassValue } from 'clsx';
import Decimal from 'decimal.js';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getErrorMessage(error: unknown) {
  if (error instanceof Error) return error.message;
  return String(error);
}

export function formatPrice(price: string): string {
  let orderTotal = Decimal(price);
  if (orderTotal.isNaN()) orderTotal = Decimal(0);
  return Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(orderTotal.toNumber());
}

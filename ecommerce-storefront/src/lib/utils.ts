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

export function formatPrice(price: string | number | Decimal): string {
  let orderTotal = Decimal(price);
  if (orderTotal.isNaN()) orderTotal = Decimal(0);
  return Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(orderTotal.toNumber());
}

const statusColors: Record<string, string> = {
  pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100',
  shipped: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100',
  delivered: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100',
  canceled: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100',
};

export function getStatusColor(status: string) {
  const unknownColor = 'bg-gray-100 text-gray-800 border-gray-200';
  return statusColors[status.toLowerCase()] || unknownColor;
}

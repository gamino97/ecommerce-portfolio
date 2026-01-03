import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  // Runs before each test and signs in each page.
  await page.goto('http://localhost:3000/login');
  await page.getByRole('textbox', { name: 'Email' }).fill('test.user1@example.com');
  await page.getByRole('textbox', { name: 'Password' }).fill('password123');
  await page.getByRole('button', { name: 'Sign In' }).click();
});

test('testProductsDashboard', async ({ page }) => {
  await page.getByRole('link', { name: 'Products' }).click();
  await expect(page.getByRole('heading')).toContainText('Products');
  await expect(page.getByRole('main')).toContainText('Add Product');
  await expect(page.getByRole('row', { name: 'Wireless Headphones Wireless' }).getByRole('link')).toBeVisible();
  await page.getByText('Toggle SidebarProductsManage').click();
});

test('testCreateProduct', async ({ page }) => {
  await page.getByRole('link', { name: 'Products' }).click();
  await page.getByRole('link', { name: 'Add Product' }).click();
  await expect(page.getByRole('main')).toContainText('Create Product');
  await expect(page.getByRole('textbox', { name: 'Name' })).toBeEmpty();
  await expect(page.locator('input[name="price"]')).toHaveValue('0');
  await expect(page.getByRole('spinbutton', { name: 'Stock' })).toHaveValue('0');
  await page.getByRole('textbox', { name: 'Description' }).click();
  await expect(page.getByRole('textbox', { name: 'Description' })).toBeEmpty();
  await expect(page.getByRole('textbox', { name: 'Image URL' })).toBeEmpty();
  await page.getByRole('textbox', { name: 'Name' }).click();
  await page.getByRole('textbox', { name: 'Name' }).fill('Custom Product');
  await page.locator('input[name="price"]').click();
  await page.locator('input[name="price"]').fill('500.01');
  await page.getByRole('spinbutton', { name: 'Stock' }).click();
  await page.getByRole('spinbutton', { name: 'Stock' }).fill('20');
  await page.getByRole('combobox', { name: 'Category' }).click();
  await page.getByLabel('Books').getByText('Books').click();
  await page.getByRole('textbox', { name: 'Description' }).click();
  await page.getByRole('textbox', { name: 'Description' }).fill('Custom description');
  await page.getByRole('textbox', { name: 'Image URL' }).click();
  await page.getByRole('textbox', { name: 'Image URL' }).fill('https://placehold.co/600x400');
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.locator('tbody')).toContainText('Custom Product');
});

import asyncio

from sqlalchemy import select

from app.db import Category, Order, OrderItem, Product, async_session_maker
from app.users import create_user


async def seed() -> None:
    """Seed the database with initial data.

    This function is idempotent: it will not create duplicates if run multiple
    times.
    """
    user_data = {
        "email": "test.user1@example.com",
        "password": "password123",
        "is_superuser": True,
        "first_name": "Test",
        "last_name": "User",
    }
    categories_data = [
        {
            "name": "Electronics",
        },
        {
            "name": "Books",
        },
        {
            "name": "Clothing",
        },
    ]
    products_data = [
        {
            "name": "Wireless Headphones",
            "description": "Bluetooth over-ear headphones",
            "image_url": "https://via.placeholder.com/150",
            "price": 99.99,
            "stock": 25,
            "category_name": "Electronics",
        },
        {
            "name": "Science Fiction Novel",
            "description": "A thrilling sci-fi adventure",
            "image_url": "https://via.placeholder.com/150",
            "price": 15.50,
            "stock": 100,
            "category_name": "Books",
        },
        {
            "name": "T-shirt",
            "description": "100% cotton, unisex",
            "image_url": "https://via.placeholder.com/150",
            "price": 19.99,
            "stock": 50,
            "category_name": "Clothing",
        },
    ]
    existing_user = await create_user(**user_data)
    async with async_session_maker() as session:
        # Seed categories
        created_categories: list[Category] = []
        for data in categories_data:
            result = await session.execute(
                select(Category).where(Category.name == data["name"])
            )
            existing = result.scalar_one_or_none()
            if existing is None:
                category = Category(**data)
                session.add(category)
                created_categories.append(category)
            else:
                created_categories.append(existing)
        await session.flush()
        # Map category names to objects for product seeding
        category_map = {cat.name: cat for cat in created_categories}

        # Seed products
        created_products: list[Product] = []
        for data in products_data:
            result = await session.execute(
                select(Product).where(Product.name == data["name"])
            )
            existing = result.scalar_one_or_none()
            if existing is None:
                product_data = data.copy()
                # Map category name to category object
                category_name = product_data.pop("category_name", "")
                category = category_map.get(category_name)
                if category:
                    product_data["category"] = category

                product = Product(**product_data)
                session.add(product)
                created_products.append(product)
            else:
                created_products.append(existing)

        await session.flush()

        # Orders based on the original SQL example (IDs are auto-generated integers)
        orders_data = [
            {
                "status": "pending",
                "shipping_address": "123 Main St, Cityville",
            },
            {
                "status": "shipped",
                "shipping_address": "456 Elm St, Townsville",
            },
        ]
        created_orders: list[Order] = []
        for data in orders_data:
            result = await session.execute(
                select(Order).where(
                    Order.shipping_address == data["shipping_address"],
                )
            )
            existing_order = result.scalar_one_or_none()
            if existing_order is None:
                order = Order(user=existing_user, **data)
                session.add(order)
                created_orders.append(order)
            else:
                created_orders.append(existing_order)

        await session.flush()

        # Map orders by shipping address for creating order items
        orders_by_address = {
            order.shipping_address: order for order in created_orders
        }

        # Order items (no price column in the current model, only quantity)
        order_items_specs = [
            {
                "shipping_address": "123 Main St, Cityville",
                "product": created_products[0],
                "quantity": 1,
                "order": created_orders[0],
            },
            {
                "shipping_address": "123 Main St, Cityville",
                "product": created_products[1],
                "quantity": 1,
                "order": created_orders[0],
            },
            {
                "shipping_address": "456 Elm St, Townsville",
                "product": created_products[2],
                "quantity": 1,
                "order": created_orders[1],
            },
        ]

        for spec in order_items_specs:
            order = orders_by_address.get(spec["shipping_address"])
            product: Product = spec["product"]
            if order is None or product is None:
                print(
                    f"Skipping order item: order or product not found for shipping address {spec['shipping_address']}"
                )
                continue
            result = await session.execute(
                select(OrderItem).where(
                    OrderItem.order_id == order.id,
                    OrderItem.product_id == product.id,
                )
            )
            existing_item = result.scalar_one_or_none()
            if existing_item is None:
                print(
                    f"Creating order item for order {order.id}, product {product.name}, quantity {spec['quantity']}"
                )
                session.add(
                    OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=spec["quantity"],
                        price=product.price * spec["quantity"],
                    )
                )
        await session.commit()


if __name__ == "__main__":
    print("Starting seed...")
    try:
        asyncio.run(seed())
        print("Seed completed successfully.")
    except Exception as e:
        print(f"Seed failed with error: {e}")
        raise

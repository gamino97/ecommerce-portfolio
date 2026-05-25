docker exec -it ecommerce-portfolio-ecommerce-portfolio-backend-1 uv run alembic upgrade head
docker exec -it ecommerce-portfolio-ecommerce-portfolio-backend-1 uv run seed.py

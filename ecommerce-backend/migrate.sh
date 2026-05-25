# Do not use % signs as your password.
sudo docker exec -it ecommerce-portfolio-ecommerce-portfolio-backend-1 uv run alembic upgrade head
sudo docker exec -it ecommerce-portfolio-ecommerce-portfolio-backend-1 uv run seed.py

# Headless E-Commerce Portfolio

A modern, scalable headless e-commerce solution built with a **Next.js** admin dashboard and a **FastAPI** backend. This project showcases a clear separation of concerns, modern architecture, and a premium user interface.

## 🏗 Architecture

The project is structured as a monorepo containing:

- **`ecommerce-admin`**: A comprehensive Admin Dashboard for managing products, orders, and customers. Built with Next.js 16 and Tailwind CSS 4.
- **`ecommerce-backend`**: A robust REST API providing business logic, data persistence, and authentication. Built with Python and FastAPI.

## 🚀 Tech Stack

### Frontend (Admin Dashboard)
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **UI Components**: Radix UI Primitives, Lucide Icons
- **State/Forms**: React Hook Form, Zod Validation

### Backend (API)
- **Framework**: FastAPI
- **Language**: Python
- **Database**: PostgreSQL (with SQLAlchemy & Alembic for migrations)
- **Package Manager**: uv
- **Testing**: pytest

## 🛠 Getting Started

### Prerequisites
- Docker Engine & Docker Compose
- Node.js & pnpm (for local frontend dev)
- Python & uv (for local backend dev)

### Quick Start (Docker)

The easiest way to perform a full system spin-up is using Docker Compose.

```bash
docker compose -f docker-compose.dev.yaml up -d
```

This will start:
- Postgres Database
- Backend API (usually on port 8000)
- Admin Dashboard (usually on port 3000)

### Local Development

#### Backend setup
1. Navigate to the backend directory:
   ```bash
   cd ecommerce-backend
   ```
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Run migrations:
   ```bash
   uv run alembic upgrade head
   ```
4. Start the server:
   ```bash
   uv run fastapi dev app/main.py
   ```

#### Admin Dashboard setup
1. Navigate to the admin directory:
   ```bash
   cd ecommerce-admin
   ```
2. Install dependencies:
   ```bash
   pnpm install
   ```
3. Start the development server:
   ```bash
   pnpm dev
   ```

## 📂 Project Structure

```
.
├── docker-compose.dev.yaml   # Container orchestration
├── ecommerce-admin/          # Next.js Application
│   ├── src/app/              # App Router Pages
│   └── ...
└── ecommerce-backend/        # FastAPI Application
    ├── app/                  # API Source Code
    ├── alembic/              # Database Migrations
    └── ...
```

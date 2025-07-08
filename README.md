# 📊 Budget Management System

A Django-based system for managing advertising campaign budgets with daily/monthly limits and time-based activation (dayparting). Built with Django, Celery, Redis, PostgreSQL, and Docker.

---

## 🚀 Quick Start

### 1. 📦 Clone and Setup

```bash
git clone https://github.com/Muneeb147/budget-management-system.git
cd budget-management-system
```

Edit `.env` with appropriate values if needed.

### 2. 🐳 Start with Docker

```bash
docker-compose up --build
```

This will run:

- Django app on [http://localhost:8000](http://localhost:8000)
- PostgreSQL on `localhost:5432`
- Redis on `localhost:6379`
- Celery worker & beat scheduler

So it'll spawn 5 containers (added as services in docker-compose.yml)

---

## ⚙️ Makefile Commands (Optional as docker compose will do the setup already)

```bash
make install       # Install dependencies
make migrate       # Run migrations
make run           # Run Django dev server
make format        # Format code with black
make lint          # Lint using flake8
...
```

---

## 🧪 Seed the Database

Create demo brands, campaigns, spends, and dayparting schedules:

```bash
docker-compose exec web python manage.py seed_data --brands=2 --campaigns=10 --spend-days=7 --daily-budget=75 --monthly-budget=1500
```

### Available arguments:

- `--brands`: Number of brands
- `--campaigns`: Total campaigns (will be evenly split)
- `--daily-budget`: Budget per campaign (default: 100)
- `--monthly-budget`: Monthly budget (default: 2500)
- `--spend-days`: Number of spend records per campaign (past days)

---

## 🔗 Connect to PostgreSQL Database

To connect to the running Postgres container using `psql`:

```bash
docker-compose exec postgres psql -U budget_user -d budget_db
```

## ❌ Reset/Clear the Data from Database

```bash
docker-compose exec web python manage.py purge_seeded_data
```



Once inside the interactive shell, you can inspect tables:

```sql
\dt                          -- list all tables
SELECT * FROM core_app_brand;
SELECT * FROM core_app_campaign LIMIT 5;
\q    
```

---

## 🕒 Celery Tasks

Celery handles:

- Budget checks
- Dayparting activation/deactivation

---

## 🧼 Code Style

- Python 3.11+
- Follows PEP8 with `black` + `flake8`
- Type hints supported via `django-stubs`

---

## 📁 Project Structure

```
budget_management_system/
├── core_app/               # Main app: models, tasks, services
├── manage.py
├── docker-compose.yml
├── Makefile
├── .env
└── requirements.txt
```


# 📘 Budget Management System – Architecture & Assumptions

---

## 🧱 Tech Stack

| Component         | Technology                 |
|------------------|----------------------------|
| Web Framework     | Django                     |
| Background Jobs   | Celery + Celery Beat       |
| Database          | PostgreSQL                 |
| Task Queue        | Redis                      |
| Timezone Handling | pytz                       |
| Dev Environment   | Docker + Docker Compose    |

---

## 🗃️ Data Model Overview

### 1. **Brand**
- Has optional `daily_budget` and `monthly_budget`
- One-to-many relationship with Campaigns

### 2. **Campaign**
- Has its own optional `daily_budget` and `monthly_budget`
- Status: `ACTIVE`, `PAUSED_BY_SYSTEM`, `PAUSED_BY_USER`
- Optional **dayparting** via `is_dayparting_enabled`

### 3. **Spend**
- Records actual `daily_spend` and `monthly_spend` for a campaign
- Unique per (`campaign`, `date`)

### 4. **DaypartingSchedule**
- Time windows (`start_time` to `end_time`) for each day of week
- Per campaign with associated `timezone`

---

## 🔄 Data Flow Assumptions

- **Spend Data** is updated externally via ETL, API, or webhook — the system **reads** from it but **does not calculate it** internally.
- Campaigns are checked **periodically via Celery** tasks to ensure:
  - Spending is within limits
  - Dayparting is respected
  - Reset/Reactive the campaign at day/month start
- Campaigns violating limits are paused by the system.

---

## 🧠 Task Scheduling (Celery)

- **`check_all_campaign_budgets`**:  
  Runs every 10 minutes. Validates each campaign’s spend and enforces limits.
- **`reactivate_monthly_campaigns`**:  
  Runs every start of month to reactivate the campaign if applicable and allowed
- **`reactivate_daily_campaigns`**:  
  Runs every start of month to reactivate the campaign if applicable and allowed
- **`enforce_dayparting_for_all_campaigns`**:  
  Also scheduled periodically. Pauses or resumes campaigns based on current time vs defined dayparting windows.

---

## ⚙️ Deployment & Dev Setup

- Managed via `docker-compose.yml` with:
  - `web` (Django app)
  - `postgres` (database)
  - `redis` (broker)
  - `celery` (worker)
  - `beat` (scheduler)

- Local development uses `.env` for secrets and database config.
- Seed data available via custom Django management command:
- `python manage.py seed_data --brands=2 --campaigns=10 --spend-days=7 --daily-budget=75 --monthly-budget=1500`

---

## 📌 Key Design Assumptions

- **One ad per campaign** (simplified model)
- Campaigns can have either `daily_budget` or `monthly_budget` or both
- Spend is externally populated (no internal cost aggregation logic)
- All budget values are assumed to be in **USD**
- Only current-day data is validated by background jobs

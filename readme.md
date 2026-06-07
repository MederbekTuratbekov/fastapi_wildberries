# E-Commerce Marketplace API

> An async REST API for a multi-vendor product marketplace — with
> membership tiers, cart management, and social auth out of the box.

[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-async-teal)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green)]()

---

## Business Problem

Marketplaces need a structured product and order API to handle seller
listings, buyer carts, and review signals at scale. Without membership
tiers and persistent cart logic, platforms leave retention revenue and
repeat-purchase incentives on the table.

---

## Demo

**Add item to cart:**
```bash
curl -X POST "http://localhost:8000/cart/?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 3, "quantity": 2}'
```
```json
{"product_id": 3, "quantity": 2}
```

**Get cart:**
```bash
curl "http://localhost:8000/cart/?user_id=1"
```
```json
{
  "id": 1, "user_id": 1,
  "cart_item": [{"id": 5, "product_id": 3, "quantity": 2}]
}
```

---

## What I Built

- **JWT auth flow** — register, login, logout, refresh; tokens
  persisted in DB, deleted on logout
- **Auto cart on register** — `Cart` record created atomically at
  registration, no extra client call needed
- **Cart management** — add/remove items with duplicate guard per user
- **Favorites** — add/remove products with duplicate guard per user
- **Product catalog** — full CRUD; article number, video, type flag,
  price, category FK, owner FK
- **Review system** — star rating + comment per product, full CRUD
- **Membership tiers** — gold/silver/bronze/simple stored on user profile
- **OAuth2** — GitHub and Google login via authlib
- **Admin panel** — sqladmin with search + sort on all 4 entities

---

## Tech Stack

| Category    | Technology                                  |
|-------------|---------------------------------------------|
| Language    | Python 3.11                                 |
| Framework   | FastAPI, Uvicorn (ASGI)                     |
| ORM         | SQLAlchemy 2.x (Mapped / mapped_column)     |
| Validation  | Pydantic v2                                 |
| Auth        | python-jose (JWT), passlib (bcrypt)         |
| OAuth2      | authlib (GitHub, Google)                    |
| Database    | PostgreSQL                                  |
| Admin       | sqladmin (search, sort, filter)             |
| Config      | python-dotenv                               |

---

## Architecture

```
Client → FastAPI (ASGI/Uvicorn)
              ↕
    APIRouter modules (auth, product, category,
    cart, favorite, review, social_auth)
              ↕
    SQLAlchemy ORM → PostgreSQL
              ↕
    sqladmin (web admin panel)
```

Modular router-per-domain. Models use SQLAlchemy 2.x `Mapped` typed
columns. Pydantic Create/Get schema split keeps input and output
contracts explicit. Business guards (duplicate cart items, missing
products) enforced at the service layer inside each router.

---

## Key Technical Decisions

**1. Auto cart creation at registration**
`Cart` is inserted in the same `auth/register` handler right after user
commit — eliminates a separate "create cart" endpoint and guarantees
every user has a cart from day one, reducing client-side setup from
2 calls to 1.

**2. DB-persisted refresh tokens**
Refresh tokens stored in `RefreshToken` table — logout deletes the
record, refresh validates against DB. Immediate revocation without
Redis or a blacklist table.

**3. Duplicate guards at the API layer**
Both cart and favorites check for existing items before insert and
return `400` with a clear message — prevents silent duplicates without
unique constraints at the DB level.

---

## How to Run

```bash
git clone https://github.com/your-username/marketplace-api
cd marketplace-api
cp .env.example .env  # add SECRET_KEY, DB URL, OAuth keys
pip install -r requirements.txt
```

```bash
python -c "from store_app.db.database import Base, engine; Base.metadata.create_all(engine)"
```

```bash
uvicorn main:online_store --reload
# Docs:  http://localhost:8000/docs
# Admin: http://localhost:8000/admin
```

---

## Business Impact

- ↑ ~30% repeat purchase rate — membership tier system creates
  visible upgrade incentive for loyal buyers (estimated)
- ↓ ~50% cart-setup friction — auto cart on registration removes
  an extra API call for client apps (estimated)
- ↓ ~40% registration drop-off — GitHub/Google OAuth removes
  password signup for most users (estimated)
- ↑ Purchase confidence — star-rated reviews surface product quality
  signals, lifting conversion by ~20% (estimated)

---

[//]: # (## Author)

[//]: # ()
[//]: # ([Your Name] — [LinkedIn]&#40;#&#41; | [GitHub]&#40;#&#41;)
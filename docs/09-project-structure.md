# 09 — Loyiha papka strukturasi

> FastAPI + SQLAlchemy (async) ekotizimida keng tan olingan **domain-based ("src layout")** struktura tanlangan — fayl turi bo'yicha emas (`routers/`, `models/`, `schemas/`), balki domain (biznes soha) bo'yicha bo'linadi. Bu loyiha kattalashganda ancha skalalanadi va domain'lar orasidagi bog'liqlikni aniq ko'rsatadi.

## 1. Umumiy struktura

```
iticket-backend/
├── src/
│   ├── auth/
│   │   ├── router.py           # /auth/* endpointlar
│   │   ├── schemas.py          # Pydantic: RegisterRequest, LoginResponse...
│   │   ├── service.py          # ro'yxatdan o'tish/login biznes logikasi
│   │   ├── security.py         # JWT yaratish/tekshirish, parol hash
│   │   ├── dependencies.py     # get_current_user, require_roles
│   │   ├── exceptions.py       # InvalidCredentialsError va h.k.
│   │   └── constants.py
│   ├── users/
│   ├── organizers/
│   ├── venues/
│   ├── categories/
│   ├── events/
│   ├── ticket_types/
│   ├── orders/
│   ├── tickets/
│   ├── payments/
│   │   ├── router.py
│   │   ├── service.py           # umumiy to'lov logikasi
│   │   └── providers/
│   │       └── demo.py          # demo/mock to'lov provayderi (MVP)
│   │           # 🎓 bonus: payme.py, click.py — real integratsiya ([[06-payment-integration.md]])
│   ├── checkin/
│   ├── notifications/
│   │   ├── service.py
│   │   ├── templates/           # Jinja2 email shablonlari
│   │   └── email_client.py
│   ├── admin/
│   ├── core/
│   │   ├── config.py             # pydantic-settings orqali .env
│   │   ├── database.py           # async engine, session factory
│   │   ├── security.py           # umumiy xavfsizlik utilities
│   │   └── exceptions.py         # global exception handler
│   ├── tasks/                    # BackgroundTasks yordamchi funksiyalari
│   │   ├── email_tasks.py        # send_order_confirmation_email(order_id)
│   │   └── ticket_tasks.py       # generate_ticket_and_notify(order_id)
│   │       # — alohida process/worker EMAS, shu FastAPI process ichida ishlaydi
│   └── main.py                   # FastAPI app, router'larni ulash
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py               # test DB, fixture'lar
│   ├── unit/
│   └── integration/
├── scripts/
│   └── seed_data.py              # dev uchun boshlang'ich ma'lumot
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/                         # ushbu hujjatlar to'plami
├── alembic.ini
├── .env.example
├── pyproject.toml
└── README.md
```

## 2. Har bir domain paketi ichida (standart shablon)

```
events/
├── router.py         # FastAPI APIRouter, faqat HTTP qatlami
├── schemas.py        # Pydantic v2: EventCreate, EventRead, EventUpdate
├── models.py          # SQLAlchemy ORM model (Event)
├── service.py         # biznes logika (yaratish, tahrirlash, publish qilish)
├── repository.py      # DB so'rovlari (kichik domain'larda service bilan birlashishi mumkin)
├── dependencies.py    # domain-specific dependency (masalan get_event_or_404)
└── exceptions.py       # EventNotFoundError, EventNotOwnedError
```

**Qoida**: `router.py` hech qachon to'g'ridan-to'g'ri SQLAlchemy session bilan so'rov yozmaydi — har doim `service.py` orqali o'tadi. Bu testlashni osonlashtiradi (service'ni router'siz test qilish mumkin).

## 3. Asosiy kutubxonalar (tavsiya)

| Vazifa | Kutubxona |
|---|---|
| Web framework | `fastapi` |
| ASGI server | `uvicorn` (dev), `gunicorn + uvicorn workers` (prod) |
| ORM | `sqlalchemy[asyncio]` 2.x |
| DB driver | `asyncpg` |
| Migratsiya | `alembic` |
| Validatsiya/schema | `pydantic` v2, `pydantic-settings` |
| Parol hash | `pwdlib` (yoki `passlib[argon2]`) |
| JWT | `python-jose` yoki `pyjwt` |
| Fon vazifalar | FastAPI o'rnatilgan `BackgroundTasks` — qo'shimcha kutubxona kerak emas |
| Email | `aiosmtplib` + `jinja2` |
| QR generatsiya | `qrcode[pil]` |
| Logging | Python o'rnatilgan `logging` moduli |
| Test | `pytest`, `pytest-asyncio`, `httpx` (ASGI test client) |
| Lint/format | `ruff` |
| Type check | `mypy` |

> 🎓 **Bonus** (loyiha kattalashganda): `arq`/`celery` + Redis (queue-based background job), `structlog` + Sentry (monitoring), `slowapi` (rate limiting).

## 4. `main.py` — yig'ish nuqtasi

```python
app = FastAPI(title="iticket.uz API")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["payments"])
app.include_router(checkin.router, prefix="/api/v1/checkin", tags=["checkin"])
app.include_router(organizer.router, prefix="/api/v1/organizer", tags=["organizer"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
# ...
```

## Bog'liq hujjatlar

[[02-architecture.md]] · [[03-database-schema.md]] · [[11-deployment-devops.md]]

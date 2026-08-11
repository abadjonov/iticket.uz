# 12 — MVP Roadmap

> Bosqichlar ketma-ket, har biri oldingisiga bog'liq — shu tartibda o'rganish/qurish tavsiya etiladi.

## Phase 0 — Loyiha skeleti

- Repo tuzilishi ([[09-project-structure.md]]), `pyproject.toml`, `ruff` sozlash.
- `docker-compose` (FastAPI + PostgreSQL).
- `core/config.py` (pydantic-settings), `core/database.py` (async engine/session).
- Alembic sozlash, birinchi bo'sh migratsiya.
- Base Pydantic schema va SQLAlchemy model pattern.

## Phase 1 — Core: Auth + Events

- `users`, `organizers` jadvallari va migratsiyalari.
- Auth: register/login/refresh, parol hash, JWT.
- `venues`, `categories` (boshlang'ich ma'lumot `scripts/seed_data.py` orqali qo'shiladi).
- `events` CRUD (organizer uchun) + public listing/search/filter.
- `ticket_types` CRUD.
- RBAC dependency'lar ([[05-rbac.md]]).

**Natija**: organizer event yaratib publish qila oladi, customer eventlarni ko'ra/qidira oladi.

## Phase 2 — Order + Demo to'lov

- `orders` jadvali (bitta ticket_type + miqdor).
- `POST /payments/demo/pay` — demo to'lov, `orders.status=paid`, oversell'siz `quantity_sold` yangilanishi.

**Natija**: customer to'liq ticket sotib olish va (demo) to'lash oqimini bajara oladi.

## Phase 3 — QR Ticketing + Check-in

- `tickets` jadvali, to'lovdan keyin `BackgroundTasks` orqali avtomatik ticket + QR generatsiya.
- QR yetkazish (email ilova + dashboard endpoint).
- `/checkin/scan` endpoint, concurrency-safe validatsiya.
- `checkin_logs`, organizer uchun check-in statistikasi.

**Natija**: to'liq uchidan-uchigacha oqim ishlaydi — sotib olish → QR olish → eventda check-in.

## Phase 4 — Email bildirishnoma

- `notifications` jadvali, `BackgroundTasks` orqali asinxron email yuborish.
- Order confirmation va organizer approval shablonlari.

## Phase 5 — Minimal admin panel

- Organizer ariza moderatsiyasi (`GET/PATCH /admin/organizers`).

## Phase 6 — Deploy

- Sodda `docker-compose` (api + postgres) production'ga chiqarish.
- `/health` endpoint, asosiy `logging`.
- Pilot event bilan to'liq uchidan-uchigacha sinov (PRD §6 muvaffaqiyat mezoni).

## 🎓 Bonus / keyingi bosqichlar (MVP tugagach)

MVP ishlagandan so'ng, quyidagilarni birma-bir qo'shib borish — har biri alohida "o'rganish sprinti" bo'lishi mumkin:

| # | Bonus vazifa | Nima o'rgatadi |
|---|---|---|
| 1 | Haqiqiy Payme/Click integratsiyasi ([[06-payment-integration.md]] §4) | Tashqi API, webhook, JSON-RPC, imzo tekshiruvi |
| 2 | To'liq admin panel (event moderatsiyasi, foydalanuvchi boshqaruvi, statistika) | Kattaroq CRUD, dashboard so'rovlari |
| 3 | Event reminder (scheduled email) | Scheduler/cron (APScheduler yoki ARQ) |
| 4 | Cart / multi-item order (`order_items` jadvali) | Murakkabroq DB modellashtirish, tranzaksiyalar |
| 5 | Redis cache + rate limiting | Performance va xavfsizlik amaliyoti |
| 6 | Sentry + structured logging | Monitoring/observability |
| 7 | Seat-map, SMS, refund, mobil ilova | Kattaroq mahsulot funksiyalari |

## Bog'liq hujjatlar

[[01-prd.md]] · [[02-architecture.md]] · [[00-index.md]]

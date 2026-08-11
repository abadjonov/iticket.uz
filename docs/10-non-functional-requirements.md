# 10 — Funksional bo'lmagan talablar (NFR)

> MVP uchun eng muhim, asosiy amaliyotlarga e'tibor qaratiladi. Enterprise-darajadagi mavzular (monitoring, rate limiting, scalability) 🎓 bonus sifatida belgilangan — bular real ish beruvchilar talab qiladigan narsalar, lekin o'quv MVP'sida shart emas.

## 1. Xavfsizlik

- **Autentifikatsiya**: JWT (access + refresh token), access token qisqa muddatli.
- **Parol saqlash**: `argon2`/`bcrypt` orqali hash (hech qachon plain-text saqlanmaydi).
- **RBAC**: [[05-rbac.md]] bo'yicha rol asosidagi ruxsatlar, har bir yozuv/tahrirlash endpointida ownership tekshiruvi.
- **CORS**: faqat ruxsat etilgan domenlar (frontend) uchun ochiq.
- **Sirlar**: barcha kalitlar (`DATABASE_URL`, `JWT_SECRET`) `.env` orqali, kodda hech qachon hardcode qilinmaydi.
- **QR token xavfsizligi**: taxmin qilib bo'lmaydigan, hech qachon public API javoblarida oshkor qilinmaydi ([[07-qr-checkin.md]]).

> 🎓 **Bonus**: rate limiting (`slowapi`), webhook imzo tekshiruvi (real to'lov integratsiyasi bilan birga keladi), audit log, PII maskalash.

## 2. Performance

- Stack **to'liq async** (FastAPI + SQLAlchemy async + asyncpg) — I/O-bound operatsiyalarda yuqori parallellik.
- DB connection pooling (SQLAlchemy async engine standart pool sozlamalari yetarli).
- N+1 so'rov muammosining oldini olish: `selectinload`/`joinedload` bilan bog'liq obyektlarni oldindan yuklash.
- Pagination barcha ro'yxat endpointlarida majburiy (default 20, max 100).
- Og'ir amallar (email, QR generatsiya) `BackgroundTasks`ga chiqariladi — API javob vaqtiga ta'sir qilmaydi.

> 🎓 **Bonus**: Redis cache (event listing), CDN, read-replica — trafik oshganda kerak bo'ladi.

## 3. Ishonchlilik (Reliability)

- `/health` endpointi — server va DB ulanishi ishlab turganini tekshirish uchun.
- Tashqi chaqiruvlar (SMTP) uchun oddiy try/except + log — xato bo'lsa `notifications.status=failed`.

## 4. Observability (kuzatuvchanlik)

- Python o'rnatilgan `logging` moduli — asosiy amallar (order yaratildi, to'lov o'tdi, check-in bo'ldi) log qilinadi.
- FastAPI avtomatik `/docs` (Swagger UI) — API'ni qo'lda sinash uchun.

> 🎓 **Bonus**: Sentry (avtomatik xatolik yig'ish), structured JSON logging (`structlog`), Prometheus metrics.

## 5. Testing strategiyasi

- **Framework**: `pytest` + `pytest-asyncio`.
- **Asosiy test turi**: integration testlar — `httpx.AsyncClient` orqali to'liq oqimni tekshirish (masalan: register → login → order → demo to'lov → check-in).
- **Test DB**: alohida `iticket_test` bazasi.
- Har bir yangi endpoint uchun kamida bitta "happy path" (muvaffaqiyatli holat) va bitta "xato holati" (masalan yetarli joy yo'q) testi yozish tavsiya etiladi — bu talabaga TDD (test-driven) fikrlashni o'rgatadi.

> 🎓 **Bonus**: unit testlar (service qatlami, mock repository bilan), CI'da avtomatik test, coverage hisoboti.

## Bog'liq hujjatlar

[[02-architecture.md]] · [[05-rbac.md]] · [[06-payment-integration.md]]

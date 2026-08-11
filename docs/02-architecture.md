# 02 — Texnik arxitektura

> MVP uchun arxitektura ataylab **minimal** tutilgan: bitta FastAPI process, bitta PostgreSQL baza, qo'shimcha infratuzilma (Redis, alohida worker, tashqi to'lov API) yo'q. Bu talabaga butun oqimni (so'rov → biznes logika → DB → javob) bitta process ichida to'liq kuzatish imkonini beradi.

## 1. Umumiy komponentlar diagrammasi

```mermaid
flowchart LR
    Client["Web Client<br/>(SPA / brauzer)"] -->|HTTPS| API["FastAPI (Uvicorn)"]
    API --> DB[("PostgreSQL<br/>asyncpg")]
    API -->|"BackgroundTasks<br/>(shu process ichida)"| BG["Email yuborish +<br/>QR generatsiya"]
    BG --> Storage[("Local disk<br/>/media — poster, QR PNG")]
    BG --> Email["Email SMTP"]
```

**Komponentlar tavsifi:**

| Komponent | Vazifasi |
|---|---|
| FastAPI (Uvicorn) | Yagona backend server — barcha so'rovlarni qabul qiladi va javob qaytaradi |
| PostgreSQL (asyncpg) | Yagona ma'lumotlar bazasi |
| FastAPI `BackgroundTasks` | So'rov javob qaytargandan keyin, **shu process ichida**, qo'shimcha vazifalarni bajaradi (email yuborish, QR generatsiya) — alohida worker/queue kerak emas |
| Local disk (`/media`) | Event poster rasmlari va generatsiya qilingan QR PNG fayllari |
| Email SMTP | Bildirishnoma yuborish uchun oddiy SMTP (dev'da Mailhog/console orqali ham tekshirish mumkin) |

> 🎓 **Bonus**: loyiha kattalashsa (yuzlab bir vaqtdagi email/QR so'rovi bo'lsa), `BackgroundTasks` o'rniga Redis + ARQ/Celery kabi alohida navbat (queue) tizimiga o'tish mumkin — bu real production loyihalarda keng qo'llaniladi, lekin MVP hajmida ortiqcha murakkablik.

## 2. Nima uchun `BackgroundTasks` yetarli?

FastAPI'ning o'rnatilgan [`BackgroundTasks`](https://fastapi.tiangolo.com/tutorial/background-tasks/) — so'rovga javob qaytarilgandan **keyin**, lekin hali shu process ichida bajariladigan funksiya. Masalan:

```python
@router.post("/payments/demo/pay")
async def pay(order_id: UUID, background_tasks: BackgroundTasks, ...):
    # ... to'lovni tasdiqlash, order.status = "paid" ...
    background_tasks.add_task(generate_ticket_and_notify, order_id)
    return {"status": "paid"}
```

Bu MVP uchun yetarli: alohida Redis, worker process, deployment murakkabligi kerak emas. Kamchiligi — agar server qayta ishga tushib qolsa, bajarilmagan background task yo'qoladi (production'da bu muammo, lekin o'quv loyihasi uchun muhim emas).

## 3. Qatlamli arxitektura (har bir domain ichida)

```
Router (FastAPI endpoint)
   │  — HTTP so'rov/javob, Pydantic schema validatsiyasi
   ▼
Service (biznes logika)
   │  — qoidalar, tranzaksiyalar, boshqa service'larni chaqirish
   ▼
Repository (DB access)
   │  — SQLAlchemy so'rovlari, CRUD
   ▼
Model (SQLAlchemy ORM)
```

- **Router** — faqat HTTP qatlami: request qabul qilish, dependency orqali auth/DB session olish, service chaqirish, response qaytarish.
- **Service** — biznes qoidalar shu yerda (masalan: "order yaratishda ticket miqdori yetarli ekanligini tekshirish").
- **Repository** — faqat ma'lumotlar bazasi bilan ishlash (query'lar).
- **Schemas** (Pydantic v2) — request/response validatsiyasi.

Batafsil papka strukturasi: [[09-project-structure.md]]

## 4. Fayl saqlash

- Event poster rasmlari va QR PNG fayllari **local disk**da (`./media/`) saqlanadi, FastAPI static mount orqali uzatiladi.
- 🎓 **Bonus**: production'ga chiqarilganda S3/MinIO kabi object storage'ga o'tish tavsiya etiladi (disk serverga bog'lab qo'ymaslik uchun).

## 5. Logging

- Oddiy Python o'rnatilgan `logging` moduli yetarli — har bir muhim amal (order yaratildi, to'lov o'tdi, check-in bo'ldi) log qilinadi.
- 🎓 **Bonus**: production'da `structlog` (structured JSON log) va Sentry (xatoliklarni avtomatik yig'ish) qo'shiladi.

## 6. Asosiy oqimlar — sequence diagramlar

### 6.1. Ro'yxatdan o'tish

```mermaid
sequenceDiagram
    participant C as Client
    participant A as FastAPI (auth)
    participant DB as PostgreSQL

    C->>A: POST /auth/register {email, password, full_name}
    A->>DB: email band emasligini tekshirish
    A->>A: parolni hash qilish (bcrypt/argon2)
    A->>DB: users jadvaliga yozish
    A-->>C: 201 Created {user_id}
    C->>A: POST /auth/login {email, password}
    A->>DB: foydalanuvchini topish, parolni tekshirish
    A-->>C: 200 OK {access_token, refresh_token}
```

### 6.2. Ticket sotib olish + demo to'lov

```mermaid
sequenceDiagram
    participant C as Client
    participant A as FastAPI
    participant DB as PostgreSQL
    participant BG as BackgroundTasks

    C->>A: POST /orders {ticket_type_id, quantity}
    A->>DB: quantity mavjudligini tekshirish, order (status=pending, expires_at) yaratish
    A-->>C: 201 {order_id, total_amount}
    C->>A: POST /payments/demo/pay {order_id}
    A->>DB: order topiladi, summasi tekshiriladi
    A->>DB: payment yozuvi (status=success), order.status=paid, quantity_sold += n (atomic)
    A->>BG: background task: generate_ticket_and_notify(order_id)
    A-->>C: 200 {status: paid}
    BG->>DB: tickets yaratish (qr_code_token bilan)
    BG->>C: email orqali QR-kodli ticket yuboriladi
```

### 6.3. QR check-in

```mermaid
sequenceDiagram
    participant O as Organizer/Admin (scanner)
    participant A as FastAPI
    participant DB as PostgreSQL

    O->>A: POST /checkin/scan {qr_token, event_id}
    A->>DB: ticket'ni qr_token bo'yicha topish (SELECT ... FOR UPDATE)
    alt ticket topilmadi
        A-->>O: 404 invalid
    else event_id mos kelmaydi
        A-->>O: 409 wrong_event
    else status = used
        A-->>O: 409 already_used
    else status = valid
        A->>DB: status=used, used_at=now(), checked_in_by, checkin_logs yozish
        A-->>O: 200 success {ticket_holder_name, ticket_type}
    end
```

## Bog'liq hujjatlar

[[03-database-schema.md]] · [[06-payment-integration.md]] · [[09-project-structure.md]] · [[10-non-functional-requirements.md]]

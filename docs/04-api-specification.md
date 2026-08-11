# 04 — API spetsifikatsiyasi

> Barcha endpointlar `/api/v1/` prefiksi bilan boshlanadi. Bu hujjat — **loyihalash darajasidagi** spetsifikatsiya; kod yozilgach FastAPI avtomatik generatsiya qiladigan interaktiv `/docs` (Swagger) bu hujjatning "jonli" versiyasi bo'ladi.

**Auth belgilash:** 🔓 ochiq · 🔑 login talab qiladi · 🛡️ rol talab qiladi (organizer/admin) · 🎓 Bonus (MVP'dan keyin)

## 1. Auth

| Method | Path | Auth | Tavsif |
|---|---|---|---|
| POST | `/auth/register` | 🔓 | Ro'yxatdan o'tish (email, phone, password, full_name) |
| POST | `/auth/login` | 🔓 | Login → `{access_token, refresh_token}` |
| POST | `/auth/refresh` | 🔓 | Refresh token orqali yangi access token olish |
| GET | `/auth/me` | 🔑 | Joriy foydalanuvchi ma'lumotlari |
| POST | `/auth/password/forgot` 🎓 | 🔓 | Parolni tiklash uchun email yuborish |
| POST | `/auth/password/reset` 🎓 | 🔓 | Yangi parol o'rnatish |

Xatoliklar: `401` (noto'g'ri kredensial), `409` (email/phone band), `422` (validatsiya).

## 2. Users

| Method | Path | Auth | Tavsif |
|---|---|---|---|
| GET | `/users/me` | 🔑 | Profil ma'lumotlari |
| GET | `/users/me/orders` | 🔑 | Buyurtmalar tarixi |
| GET | `/users/me/tickets` | 🔑 | Foydalanuvchining barcha ticketlari |

## 3. Events (public)

| Method | Path | Auth | Tavsif |
|---|---|---|---|
| GET | `/events` | 🔓 | Ro'yxat, filtrlar: `category`, `city`, `q` (matn qidiruv), `page`, `page_size` |
| GET | `/events/{slug}` | 🔓 | Event tafsilotlari |
| GET | `/events/{event_id}/ticket-types` | 🔓 | Event uchun mavjud ticket turlari va narxlari |
| GET | `/categories` | 🔓 | Kategoriyalar ro'yxati |
| GET | `/venues` | 🔓 | Venue'lar ro'yxati |

Xatoliklar: `404` (event/slug topilmadi).

## 4. Orders & Tickets (customer)

| Method | Path | Auth | Tavsif |
|---|---|---|---|
| POST | `/orders` | 🔑 | Buyurtma yaratish: `{ticket_type_id, quantity}` → `status=pending`, `expires_at` |
| GET | `/orders/{id}` | 🔑 | Buyurtma tafsilotlari (faqat egasi) |
| GET | `/orders` | 🔑 | O'z buyurtmalari ro'yxati |
| GET | `/tickets/{id}` | 🔑 | Ticket tafsilotlari (faqat egasi) |
| GET | `/tickets/{id}/qr` | 🔑 | QR-kod rasm (PNG) |

`POST /orders` request namunasi (bitta ticket_type, MVP):
```json
{ "ticket_type_id": "uuid", "quantity": 2 }
```

Xatoliklar: `400` (yetarli joy yo'q), `403` (boshqasining buyurtmasi), `404`, `409` (allaqachon to'langan/bekor qilingan).

## 5. Payments

| Method | Path | Auth | Tavsif |
|---|---|---|---|
| POST | `/payments/demo/pay` | 🔑 | `{order_id}` → to'lovni darhol simulyatsiya qiladi (`payments` yozuvi yaratiladi, `orders.status=paid`, QR+email background task ishga tushadi) |
| GET | `/payments/{id}/status` | 🔑 | To'lov holatini tekshirish |

`POST /payments/demo/pay` javobi:
```json
{ "status": "paid", "order_id": "uuid" }
```

> 🎓 **Bonus — real to'lov integratsiyasi**: `POST /payments/payme/create`, `POST /payments/click/create` + `POST /webhooks/payme`, `POST /webhooks/click/prepare|complete` — Payme/Click Merchant API orqali. Batafsil: [[06-payment-integration.md]] ("Bonus" bo'limi).

## 6. Organizer panel

| Method | Path | Auth | Tavsif |
|---|---|---|---|
| POST | `/organizer/apply` | 🔑 | Organizer bo'lishga ariza (`status=pending`) |
| GET | `/organizer/events` | 🛡️ organizer | O'z eventlari ro'yxati |
| POST | `/organizer/events` | 🛡️ organizer | Yangi event yaratish (`status=draft`) |
| PATCH | `/organizer/events/{id}` | 🛡️ organizer | Eventni tahrirlash (faqat o'ziniki) |
| POST | `/organizer/events/{id}/publish` | 🛡️ organizer | `status: draft → published` |
| POST | `/organizer/events/{id}/ticket-types` | 🛡️ organizer | Ticket turi qo'shish |
| PATCH | `/organizer/ticket-types/{id}` | 🛡️ organizer | Ticket turini tahrirlash |
| GET | `/organizer/events/{id}/sales` 🎓 | 🛡️ organizer | Sotuv statistikasi |

Xatoliklar: `403` (organizer boshqa organizerning eventiga kirmoqchi bo'lsa — ownership check).

## 7. Admin panel (MVP'da minimal)

| Method | Path | Auth | Tavsif |
|---|---|---|---|
| GET | `/admin/organizers` | 🛡️ admin | Organizer arizalari ro'yxati (filtr: status) |
| PATCH | `/admin/organizers/{id}/approve` | 🛡️ admin | Organizer arizasini tasdiqlash/rad etish |

> 🎓 **Bonus — to'liq admin panel**: `GET /admin/users` + bloklash, `GET /admin/events` + moderatsiya, `POST /admin/venues`, `POST /admin/categories`, `GET /admin/dashboard/stats`. MVP'da venue/category boshlang'ich ma'lumotlari oddiy seed-script (`scripts/seed_data.py`) orqali qo'shilishi mumkin.

## 8. Check-in

| Method | Path | Auth | Tavsif |
|---|---|---|---|
| POST | `/checkin/scan` | 🛡️ organizer/admin | `{qr_token, event_id}` → `success/already_used/invalid/wrong_event` |
| GET | `/checkin/events/{event_id}/stats` | 🛡️ organizer/admin | Check-in statistikasi (nechta ticketdan nechtasi kirdi) |

Batafsil oqim: [[07-qr-checkin.md]].

## 9. Umumiy konventsiyalar

- **Pagination**: `page` (default 1), `page_size` (default 20, max 100); javobda `{items, total, page, page_size}`.
- **Xatolik formati**: `{"detail": "..."}` — FastAPI standart `HTTPException`.
- **Auth header**: `Authorization: Bearer <access_token>`.

## Bog'liq hujjatlar

[[03-database-schema.md]] · [[05-rbac.md]] · [[06-payment-integration.md]] · [[07-qr-checkin.md]]

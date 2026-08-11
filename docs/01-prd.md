# 01 — Product Requirements Document (PRD)

> iticket.uz — turli xil eventlarga (konsert, teatr, sport, stand-up va h.k.) online ticket sotadigan platforma. Bu — **Backend Development kursi doirasidagi o'quv/amaliyot loyihasi**. Hujjat ataylab sodda tutilgan: MVP'ni tugatib bo'lgach, "🎓 Bonus" bo'limlaridagi vazifalar orqali loyihani asta-sekin murakkablashtirib borish mumkin.

## 1. Muammo va maqsad

O'zbekistonda event tashkilotchilari ticketlarni ko'pincha qo'lda yoki norasmiy kanallar orqali sotadi — bu xaridor uchun noqulay, tashkilotchi uchun kuzatib bo'lmaydigan, eventga kirishda esa sekin va xatoga moyil.

**Maqsad**: foydalanuvchilarga eventlarni topish va ticket sotib olish, tashkilotchilarga event yaratish, kirishda esa QR-kod orqali tez tekshirish imkonini beruvchi sodda platforma qurish — va shu jarayonda FastAPI + SQLAlchemy + PostgreSQL bilan haqiqiy backend loyihasini boshidan oxirigacha qurishni o'rganish.

## 2. Foydalanuvchi rollari

| Rol | Tavsif |
|---|---|
| `customer` | Ro'yxatdan o'tgan, event qidiruvchi va ticket sotib oluvchi oddiy foydalanuvchi |
| `organizer` | Event yaratuvchi (admin tasdig'idan o'tgan `customer`) |
| `admin` | Organizer arizalarini tasdiqlovchi xodim |

Batafsil: [[05-rbac.md]].

## 3. User story'lar

**Customer sifatida:**
- Men ro'yxatdan o'tib, tizimga kira olishni istayman.
- Men shahar/kategoriya/sana bo'yicha eventlarni qidira olishni istayman.
- Men event tafsilotlarini va ticket narxlarini ko'ra olishni istayman.
- Men bitta ticket_type'dan kerakli miqdorda tanlab, buyurtma bera olishni istayman.
- Men "to'lov" tugmasini bosib (demo to'lov), darhol QR-kodli ticketimni email va shaxsiy kabinetimda ko'ra olishni istayman.
- Men o'z buyurtmalarim tarixini ko'ra olishni istayman.

**Organizer sifatida:**
- Men organizer bo'lishga ariza topshirib, admin tasdig'ini kuta olishni istayman.
- Men yangi event yaratib, ticket turlari va narxlarini belgilay olishni istayman.
- Men eventimni "draft" holatda tayyorlab, keyin "published" qila olishni istayman.
- Men event kunida QR-kodlarni skaner qilib, ticketlarni tasdiqlay olishni istayman.

**Admin sifatida:**
- Men organizer arizalarini ko'rib chiqib, tasdiqlay yoki rad eta olishni istayman.

## 4. MVP scope

### Kiradi (in-scope)
- Ro'yxatdan o'tish/kirish (email + parol, JWT).
- Event CRUD (organizer tomonidan), kategoriya va venue bilan bog'liq.
- Ticket turlari va narxlari boshqaruvi.
- Public event qidiruv/filtr.
- Order yaratish: **bitta ticket_type + miqdor** (cart emas).
- **Demo to'lov**: bitta so'rov bilan to'lovni simulyatsiya qilish (`success`/`failed`), tashqi provider kerak emas.
- To'lovdan so'ng avtomatik QR-kodli ticket generatsiyasi (FastAPI `BackgroundTasks` orqali).
- QR-kod orqali check-in (organizer/admin tomonidan skanerlash).
- Email orqali bildirishnoma (buyurtma tasdig'i) — `BackgroundTasks` orqali, request'ni bloklamasdan.
- Minimal admin panel: faqat organizer arizalarini tasdiqlash.

### 🎓 Bonus / keyingi bosqich (MVP'dan keyin qo'shish uchun)
- **Haqiqiy Payme/Click integratsiyasi** — real to'lov tizimlari, JSON-RPC/webhook, imzo tekshiruvi (bular murakkab va sandbox hisob talab qiladi).
- **To'liq admin panel** — event moderatsiyasi, foydalanuvchi boshqaruvi, statistika dashboard.
- **Event reminder** — event boshlanishidan oldin avtomatik eslatma email (scheduler/cron talab qiladi).
- **Cart / multi-item order** — bir buyurtmada bir nechta xil ticket_type sotib olish.
- **Seat-map** — aniq o'rindiq tanlash.
- **SMS bildirishnoma**.
- **Pul qaytarish (refund)** avtomatik oqimi.
- **Mobil ilova**.

## 5. Biznes qoidalar

1. Har bir `order` yaratilgach, `N=15 daqiqa` ichida to'lanmasa, avtomatik `expired` holatiga o'tadi.
2. Har bir ticket faqat bitta marta check-in qilinishi mumkin (QR bir martalik).
3. Foydalanuvchi `organizer` bo'lish uchun ariza topshiradi, faqat admin tasdiqlagandan so'ng event yarata oladi.
4. Event faqat `published` holatida public qidiruvda ko'rinadi.
5. `ticket_types.quantity_sold` hech qachon `quantity_total` dan oshmasligi kerak (oversell taqiqlanadi).

## 6. Muvaffaqiyat mezonlari (MVP uchun)

- Foydalanuvchi ro'yxatdan o'tishdan to ticket sotib olishgacha bo'lgan yo'lni to'liq bajara olishi (register → login → event topish → order → demo to'lov → QR olish → check-in).
- Kamida 1 ta demo event to'liq oqim orqali sinovdan o'tkazilishi.

## 7. Taxminlar va cheklovlar

- Faqat UZS valyutasi (raqam sifatida, real to'lov integratsiyasi yo'q).
- Faqat O'zbekiston bozori uchun mo'ljallangan (til: o'zbek).
- Bitta event bitta venue'da bo'ladi.

## Bog'liq hujjatlar

[[02-architecture.md]] · [[03-database-schema.md]] · [[04-api-specification.md]] · [[05-rbac.md]] · [[06-payment-integration.md]] · [[07-qr-checkin.md]] · [[12-roadmap.md]]

# iticket.uz — Texnik hujjatlar indeksi

**iticket.uz** — turli xil eventlarga (konsert, teatr, sport, stand-up va h.k.) online ticket sotadigan platforma. Bu — **Backend Development kursi doirasidagi o'quv/amaliyot loyihasi**: hujjatlar ataylab MVP darajasida sodda tutilgan, murakkabroq (production-darajadagi) mavzular har bir faylda "🎓 Bonus" deb alohida belgilangan — MVP tugagach ularni birma-bir qo'shib borish mumkin ([[12-roadmap.md]]).

## Tech stack (MVP)

| Qatlam | Texnologiya |
|---|---|
| Backend | Python, FastAPI (async) |
| ORM | SQLAlchemy 2.x (async) + asyncpg |
| Ma'lumotlar bazasi | PostgreSQL |
| Fon vazifalar | FastAPI o'rnatilgan `BackgroundTasks` (alohida Redis/worker yo'q) |
| To'lov | Demo (mock) provider — 🎓 Payme/Click bonus sifatida |
| Bildirishnoma | Email (SMTP) |
| Deploy | Docker (`api` + `postgres`), GitHub Actions (lint+test) |

## Hujjatlar ro'yxati (tavsiya etilgan o'qish tartibi)

1. [[01-prd.md]] — Product Requirements Document: muammo, rollar, user story'lar, MVP scope, biznes qoidalar
2. [[02-architecture.md]] — Texnik arxitektura: komponentlar, qatlamlar, sequence diagramlar
3. [[03-database-schema.md]] — DB schema / ERD, jadvallar va bog'lanishlar
4. [[04-api-specification.md]] — API endpoints spetsifikatsiyasi
5. [[05-rbac.md]] — Rollar va ruxsatlar (customer/organizer/admin)
6. [[06-payment-integration.md]] — Demo to'lov provayderi (+ Payme/Click bonus)
7. [[07-qr-checkin.md]] — QR-kod check-in oqimi
8. [[08-notifications.md]] — Email bildirishnoma oqimi
9. [[09-project-structure.md]] — Loyiha papka strukturasi
10. [[10-non-functional-requirements.md]] — Xavfsizlik, performance, testing
11. [[11-deployment-devops.md]] — Docker, CI/CD, deployment rejasi
12. [[12-roadmap.md]] — MVP bosqichlari (Phase 0-6) + Bonus ro'yxati

## Qisqacha loyiha xulosasi

Customer eventlarni qidiradi va ticket sotib oladi (bitta ticket_type + miqdor) → demo to'lov tugmasi bosilgach QR-kodli ticket avtomatik generatsiya qilinib email orqali yuboriladi → event kunida organizer/admin QR-kodni skanerlab kirishni tasdiqlaydi. Organizer admin tasdig'idan o'tgach event va ticket turlarini boshqara oladi. Admin panelning MVP'dagi yagona vazifasi — organizer arizalarini tasdiqlash.

To'liq foydalanuvchi oqimlari va texnik tafsilotlar yuqoridagi hujjatlarda batafsil yoritilgan. Har bir hujjatdagi 🎓 belgili qismlar — MVP tugagach loyihani asta-sekin murakkablashtirib borish uchun mo'ljallangan keyingi bosqichlar.

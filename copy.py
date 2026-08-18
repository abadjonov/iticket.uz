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
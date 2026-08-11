# 11 — Deployment / DevOps rejasi

> MVP uchun eng sodda deployment yetarli: bitta API konteyner + bitta PostgreSQL. Redis, worker, MinIO kabi qo'shimcha xizmatlar yo'q — bu talaba uchun Docker/deployment tushunchalarini ortiqcha murakkablashtirmasdan o'rganish imkonini beradi.

## 1. Muhitlar

| Muhit | Maqsad |
|---|---|
| **Local** | Dasturchi kompyuterida, `docker-compose` orqali |
| **Production** | Haqiqiy foydalanuvchilar uchun (masalan bitta VPS) |

> 🎓 **Bonus**: alohida **staging** muhiti — yangi funksiyalarni production'dan oldin sinash uchun, jamoa kattalashganda foydali.

## 2. Konteynerizatsiya

`docker/docker-compose.yml` xizmatlari:

```yaml
services:
  api:        # FastAPI + Uvicorn
  postgres:   # PostgreSQL
  nginx:      # reverse proxy (ixtiyoriy, prod uchun)
```

- **Dockerfile**: bitta bosqichli (yoki oddiy 2-bosqichli) build — dependency o'rnatish + kod nusxalash yetarli, murakkab multi-stage optimizatsiya shart emas.
- Local dev uchun `docker-compose.override.yml` — hot-reload (`uvicorn --reload`), volume mount bilan kod o'zgarishi darhol aks etadi.

> 🎓 **Bonus**: loyiha kattalashsa, `redis`, `worker`, `minio` xizmatlari `docker-compose.yml`ga qo'shiladi (Redis+ARQ ga o'tilganda, [[02-architecture.md]] "Bonus" izohiga qarang).

## 3. CI/CD (GitHub Actions) — sodda versiya

Pipeline bosqichlari (har bir push/PR uchun):

1. **Lint**: `ruff check .`
2. **Test**: `pytest` (alohida test PostgreSQL service container bilan)

Shu ikki bosqich MVP uchun yetarli — har bir push kodning ishlashini avtomatik tekshiradi.

> 🎓 **Bonus**: `mypy` type check, Docker image build+push, avtomatik staging deploy, production uchun qo'lda tasdiqlash bosqichi.

## 4. Migratsiya

- Deploy qilishdan oldin (yoki server ishga tushganda) `alembic upgrade head` qo'lda yoki `docker-compose` entrypoint skriptida bajariladi.

## 5. Sirlarni boshqarish

- **Local**: `.env` fayli (`.env.example` git'ga qo'shiladi, haqiqiy `.env` — `.gitignore`da).
- **CI/CD va production**: GitHub Actions Secrets — `DATABASE_URL`, `JWT_SECRET`.

## 6. Domen va SSL (production uchun, ixtiyoriy)

- Nginx reverse proxy + Let's Encrypt (`certbot`) orqali SSL sertifikat — agar loyiha haqiqiy domenga chiqarilsa.

## Bog'liq hujjatlar

[[02-architecture.md]] · [[09-project-structure.md]]

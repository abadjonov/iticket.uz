import uvicorn

from src.main import app
from src.core.config import settings


def main():
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)


if __name__ == "__main__":
    main()

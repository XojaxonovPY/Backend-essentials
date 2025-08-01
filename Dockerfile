FROM python:3.11-slim

WORKDIR /app

# Faqat kerakli fayllarni nusxalaymiz
COPY bot/ ./bot/

RUN pip install aiogram

CMD ["python", "bot/main.py"]


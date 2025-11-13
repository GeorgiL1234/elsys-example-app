# 1️⃣ Използваме официалния Python 3.13 образ
FROM python:3.13-slim

# 2️⃣ Настройка на работна директория в контейнера
WORKDIR /app

# 3️⃣ Копираме requirements.txt и го инсталираме
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4️⃣ Копираме целия проект в контейнера
COPY . .

# 5️⃣ Експонираме порт 8000 за FastAPI
EXPOSE 8000

# 6️⃣ Команда за стартиране на приложението с uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM python:3.12-slim

# Ishchi katalogni belgilash
WORKDIR /app

# Python optimizatsiyasi
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Tizim paketlarini yangilash
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Bog'liqliklarni o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha kodlarini ko'chirish
COPY . .

# Portni faqat ichki Docker tarmog'iga bildirish (VPS ochiq portlariga chiqarilmaydi)
EXPOSE 8080

# Botni ishga tushirish
CMD ["python", "app.py"]

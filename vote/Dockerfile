# TAHAP 1: BUILDER - Menginstall dependensi
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# TAHAP 2: FINAL - Hanya menjalankan aplikasi
FROM python:3.9-slim
WORKDIR /app
# Salin dependensi dari tahap builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
# Salin kode aplikasi
COPY . .
# Perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]
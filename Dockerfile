# Gunakan base image Python
FROM python:3.11-slim

# Install uv dan dependensi sistem ringan
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Buat direktori aplikasi
WORKDIR /app

# Salin semua file ke image
COPY . .

# Install paket
RUN pip install uvicorn httpx dotenv fastapi

# Jalankan script
CMD ["python", "main.py"]

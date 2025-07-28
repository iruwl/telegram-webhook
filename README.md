# TELEGRAM WEBHOOK

Skrip **Telegram Webhook** ini merupakan listener sederhana untuk menerima pesan dari Bot Telegram, kemudian meneruskan pesan tersebut ke Webhook N8N. Cocok digunakan untuk integrasi otomatis seperti notifikasi, workflow N8N, atau sistem chatbot sederhana.

---

## 🔧 Instalasi & Menjalankan

Ikuti langkah-langkah berikut untuk menyiapkan dan menjalankan proyek:

#### 1. Clone repository ini

```bash
git clone https://github.com/iruwl/telegram-webhook
```

#### 2. Masuk ke direktori proyek

```bash
cd telegram-webhook
```

#### 3. Buat Python virtual environment

```bash
python3 -m venv env
```

#### 4. Install paket yang dibutuhkan untuk menjalankan aplikasi

```bash
./env/bin/pip install uvicorn httpx dotenv fastapi
```

Contoh output:
```
Collecting uvicorn
  Using cached uvicorn-0.35.0-py3-none-any.whl (66 kB)
Installing collected packages: click, uvicorn
Successfully installed click-8.1.8 uvicorn-0.35.0
```

#### 5. Salin file `.env-example` menjadi `.env`

```bash
cp .env-example .env
```

#### 6. Edit file `.env` sesuai kebutuhan

```bash
vi .env
```

Contoh isi `.env`:

```env
# Port yang digunakan oleh aplikasi
PORT="8000"

# Token Bot Telegram
TG_BOT_TOKEN="999999999:SDMk-345msdfl mlk435mfdf_2sdklam$sd"

# URL webhook N8N (gunakan yang test/development)
N8N_WEBHOOK_URL="http://localhost:5678/webhook-test/7091c9ff-4e4d-4400-8dff-e03f77a2ba0e"

# Mode aplikasi: PROD atau TEST
N8N_MODE="PROD"
```

#### 7. Jalankan Ngrok untuk expose url lokal ke publik

```bash
ngrok http http://localhost:8000
```

Contoh output terminal:

```
ngrok                                                                                                                 (Ctrl+C to quit)

🫶 Using ngrok for OSS? Request a community license: https://ngrok.com/r/oss

Session Status                online
Account                       irul (Plan: Free)
Version                       3.25.0
Region                        Asia Pacific (ap)
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://ae87e0781a4d.ngrok-free.app -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

#### 8. Jalankan aplikasi pada terminal yang baru

```bash
./env/bin/python main.py
```

Contoh output terminal:

```
INFO 🚀 Starting server...
INFO ✔ Ngrok URL: https://ae87e0781a4d.ngrok-free.app
INFO ✔ Telegram webhook set to https://ae87e0781a4d.ngrok-free.app/webhook
INFO Application startup complete.
```

#### 9. Webhook Siap Digunakan

Jika tidak ada error pada log, maka aplikasi sudah siap menerima pesan dari Telegram dan meneruskannya ke N8N.

Contoh log ketika menerima pesan:

```
INFO ↪ Received data from Telegram: {'update_id': 2, 'message': {'text': 'hallo!'}}
INFO ✔ Message successfully sent to N8N
```

---

## 🐳 Jalankan dengan Docker

Jika kamu ingin menjalankan project ini menggunakan Docker, ikuti langkah berikut:

#### 1. Clone repository ini

```bash
git clone https://github.com/iruwl/telegram-webhook
```

#### 2. Masuk ke direktori proyek

```bash
cd telegram-webhook
```

#### 3. Salin file `.env-example` menjadi `.env` dan edit sesuai kebutuhan

```bash
cp .env-example .env
vi .env
```

#### 4. Build dan Jalankan

```
docker compose up -d
```

atau

```
docker compose up --build -d
```

#### 5. Cek log container

```
docker logs -f telegram-webhook
```

---

## 📌 Catatan

- Pastikan token bot Telegram kamu valid.
- Jangan lupa menyesuaikan URL N8N yang aktif.
- Membutuhkan ngrok untuk ekspose url lokal ke publik.
- Jika menggunakan docker, pastikan port yang digunakan sesuai dengan konfigurasi .env.

---

## 🛠 Teknologi yang Digunakan

- Ngrok
- Python 3.10+

---

## 📬 Lisensi

MIT License

---

## 🙋‍♂️ Sumber Asli

Ref: https://github.com/sjanaX01/n8n-Telegram-Bot-Webhook

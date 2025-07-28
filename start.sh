#!/bin/bash

echo "⌛ Menunggu ngrok siap..."

# Tunggu hingga ngrok API tersedia dan mengembalikan URL
while true; do
  NGROK_API=$(curl -s http://ngrok:4040/api/tunnels)
  if echo "$NGROK_API" | grep -q 'https://'; then
    NGROK_URL=$(echo "$NGROK_API" | grep -Eo 'https://[a-z0-9]+\.ngrok-free\.app' | head -n 1)
    break
  fi
  echo "⏳ Ngrok belum siap, retrying..."
  sleep 1
done

echo "🌐 Ngrok aktif di: $NGROK_URL"

# Set webhook Telegram (opsional, bisa juga dari main.py jika otomatis)
# curl -X POST "https://api.telegram.org/bot$TG_BOT_TOKEN/setWebhook" -d "url=$NGROK_URL/webhook"

# Jalankan aplikasi
echo "🚀 Menjalankan Telegram Webhook..."
exec python main.py

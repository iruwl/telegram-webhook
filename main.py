import httpx
import logging.config
import os
import uvicorn
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from uvicorn.config import LOGGING_CONFIG

log = logging.getLogger("uvicorn.error")

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
N8N_MODE = os.getenv("N8N_MODE")
RUN_MODE = os.getenv("RUN_MODE")

NGROK_HOST = "ngrok:4040" if RUN_MODE.lower() == "docker" else "127.0.0.1:4040"
WEBHOOK_URL = N8N_WEBHOOK_URL if N8N_MODE.lower() == "test" else N8N_WEBHOOK_URL.replace("-test/", "/")


async def check_ngrok():
    try:
        async with httpx.AsyncClient() as client:
            url = f"http://{NGROK_HOST}/api/tunnels"
            resp = await client.get(url)
            resp.raise_for_status()
            tunnels = resp.json().get("tunnels", [])
            if tunnels:
                public_url = tunnels[0].get("public_url")
                log.info(f"✔ Ngrok URL: {public_url}")
                return public_url
    except Exception as e:
        log.error(f"✖ Ngrok server not available: {e}")
    return None


async def setup_webhook():
    public_url = await check_ngrok()
    if not public_url:
        log.error("✖ Cannot set Telegram webhook without Ngrok URL")
        return

    webhook_url = f"{public_url}/webhook"
    api_url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/setWebhook"

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(api_url, json={"url": webhook_url})
            resp.raise_for_status()
            if resp.json().get("ok"):
                log.info(f"✔ Telegram webhook set to {webhook_url}")
            else:
                log.error(f"✖ Telegram rejected webhook setup: {resp.text}")
    except Exception as e:
        log.error(f"✖ Exception setting webhook: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_webhook()
    yield


app = FastAPI(lifespan=lifespan)


async def pass_data_to_n8n(data: dict) -> None:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(WEBHOOK_URL, json=data)
            resp.raise_for_status()
            log.info("✔ Message successfully sent to N8N")
    except httpx.HTTPStatusError as e:
        log.error(f"✖ HTTP error from N8N: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        log.error(f"✖ Failed to send message to N8N: {e}")


@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    log.info(f"↪ Received data from Telegram: {data}")
    await pass_data_to_n8n(data)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/", response_class=PlainTextResponse)
async def root():
    return "Telegram Webhook is running"


if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s %(levelname)4.4s %(message)s"
    LOGGING_CONFIG["formatters"]["access"] = {
        "format": "%(asctime)s %(levelname)4.4s %(message)s",
        "use_colors": None,
    }
    LOGGING_CONFIG["loggers"]["uvicorn.access"] = {
        "handlers": [],
        "level": "CRITICAL",
        "propagate": False,
    }
    logging.config.dictConfig(LOGGING_CONFIG)
    log.info("🚀 Starting server...")
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)

from fastapi import APIRouter, Request
from telegram import Bot, error
import os
import asyncio

router = APIRouter(prefix="/api", tags=["mensajes"])

bot = Bot(token=os.getenv("BOT_TOKEN"))

@router.post("/enviar-mensajes")
async def enviar_mensajes(request: Request):
    datos = await request.json()
    mensajes = datos.get("notificaciones", [])

    enviados = 0
    errores = []

    for item in mensajes:
        telegram_id = item.get("telegram_id")
        texto = item.get("mensaje")
        if not telegram_id or not texto:
            continue
        try:
            await bot.send_message(chat_id=telegram_id, text=texto)
            enviados += 1
        except error.TelegramError as e:
            errores.append({"telegram_id": telegram_id, "error": str(e)})

    return {
        "status": "ok",
        "mensajes_enviados": enviados,
        "errores": errores
    }

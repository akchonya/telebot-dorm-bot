import time
import asyncio
from alerts_in_ua import AsyncClient as AsyncAlertsClient
from PIL import Image


def pillow_draw(char, h, w):
    w = int(w)
    h = int(h)
    img = Image.open(f"pillow_bot/{char}.png")
    img_w, img_h = img.size


    background = Image.open("pillow_bot/vahta.jpg")
    bg_w, bg_h = background.size
    offset = (bg_w // 7 * w - img_w // 3 * 2, bg_h // 10 * (1 + h))
    background.paste(img, offset, img)
    background.save("pillow_bot/vahta.jpg")


async def alerts(ALERTS_TOKEN):
    alerts_client = AsyncAlertsClient(token=ALERTS_TOKEN)
    active_alerts = await alerts_client.get_air_raid_alert_statuses_by_oblast()
    zapor = str([alert for alert in active_alerts if alert.location_title == "Запорізька область"][0])[:-18]
    return zapor


asyncio.run(alerts())


from fastapi import FastAPI
from uvicorn import run
from db.db_setup import init_db, async_session
from routers.notifications import notification_router
import asyncio
from mq.server import srvr

app = FastAPI(docs_url='/docs')
app.include_router(notification_router)


@app.on_event('startup')
async def on_startup():
    await init_db()
    loop = asyncio.get_event_loop()
    loop.create_task(srvr(async_session()))


if __name__ == '__main__':
    run('main:app', reload=True, port=8001)

from fastapi import APIRouter, WebSocket, Depends
from mq.ws import profile_manager, user_manager
from db.db_setup import get_session
from db.utils.user import add_user_notification, get_user_notifications, get_new_user_notifications
from db.utils.profile import add_profile_notification, get_profile_notifications, get_new_profile_notifications
from datetime import datetime

notification_router = APIRouter()


@notification_router.get('/get-profile-notifications')
async def get_profile_notifications_path(profile_id: int, session=Depends(get_session)):
    return await get_profile_notifications(profile_id, session)


@notification_router.get('/get-user-notifications')
async def get_user_notifications_path(user_id: int, session=Depends(get_session)):
    return await get_user_notifications(user_id, session)


@notification_router.get('/get-new-profile-notifications')
async def get_new_profile_notifications_path(profile_id: int, time: datetime, session=Depends(get_session)):
    return await get_new_profile_notifications(profile_id, time, session)


@notification_router.get('/get-new-user-notifications')
async def get_new_user_notifications_path(user_id: int, time: datetime, session=Depends(get_session)):
    return await get_new_user_notifications(user_id, time, session)


@notification_router.websocket('/get-profile-notifications/{profile_id}')
async def get_profile_notifications_ws(ws: WebSocket, profile_id: int):
    await profile_manager.connect(ws, profile_id)
    while True:
        await ws.receive_json()


@notification_router.websocket('/get-user-notifications/{user_id}')
async def get_user_notifications_ws(ws: WebSocket, user_id: int):
    await user_manager.connect(ws, user_id)
    while True:
        await ws.receive_json()


@notification_router.post('/send-back-to-user/{user_id}/{profile_id}')
async def send_back_to_user(user_id: int, profile_id: int, session=Depends(get_session)):
    await add_user_notification(profile_id, user_id, False, session)
    await user_manager.send_personal_message({'user_id': user_id, 'profile_id': profile_id})


@notification_router.post('/send-back-to-profile/{profile_id}/{user_id}')
async def send_back_to_profile(profile_id: int, user_id: int, session=Depends(get_session)):
    await add_profile_notification(profile_id, user_id, False, session)
    await profile_manager.send_personal_message({'profile_id': profile_id, 'user_id': user_id})

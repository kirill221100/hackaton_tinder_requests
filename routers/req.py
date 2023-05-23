from fastapi import APIRouter, WebSocket, Depends
from mq.ws import profile_manager, user_manager
from db.db_setup import get_session
from db.utils.to_user import add_req_to_user, get_user_notifs
from db.utils.to_profile import add_req_to_profile, get_profile_notifs

req_router = APIRouter()


@req_router.get('/get-profile-notifications')
async def get_requests_to_profile(profile_id: int, session=Depends(get_session)):
    return await get_profile_notifs(profile_id, session)


@req_router.get('/get-user-notifications')
async def get_requests_to_user(user_id: int, session=Depends(get_session)):
    return await get_user_notifs(user_id, session)


@req_router.websocket('/get-profile-notifications/{profile_id}')
async def get_requests_to_profile_ws(ws: WebSocket, profile_id: int):
    await profile_manager.connect(ws, profile_id)
    while True:
        await ws.receive_json()


@req_router.websocket('/get-user-notifications/{user_id}')
async def get_requests_to_user_ws(ws: WebSocket, user_id: int):
    await user_manager.connect(ws, user_id)
    while True:
        await ws.receive_json()


@req_router.post('/send-back-to-user/{user_id}/{profile_id}')
async def send_back_to_user(user_id: int, profile_id: int, session=Depends(get_session)):
    await add_req_to_user(profile_id, user_id, False, session)
    await user_manager.send_personal_message({'user_id': user_id})


@req_router.post('/send-back-to-profile/{profile_id}/{user_id}')
async def send_back_to_profile(profile_id: int, user_id: int, session=Depends(get_session)):
    await add_req_to_profile(profile_id, user_id, False, session)
    await profile_manager.send_personal_message({'profile_id': profile_id})

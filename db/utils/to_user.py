from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.req import ToUser


async def add_req_to_user(profile_id: int, user_id: int, is_request: bool, session: AsyncSession):
    req = ToUser(profile_id=profile_id, user_id=user_id, is_request=is_request)
    session.add(req)
    await session.commit()


async def get_user_notifs(user_id: int, session: AsyncSession):
    return (await session.execute(select(ToUser).filter(ToUser.user_id == user_id).order_by(ToUser.id.desc())
                                  .limit(20))).scalars().all()

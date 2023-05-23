from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.req import ToProfile


async def add_req_to_profile(profile_id: int, user_id: int, is_request: bool, session: AsyncSession):
    req = ToProfile(profile_id=profile_id, user_id=user_id, is_request=is_request)
    session.add(req)
    await session.commit()


async def get_profile_notifs(profile_id: int, session: AsyncSession):
    return (await session.execute(select(ToProfile).filter(ToProfile.profile_id == profile_id)
                                  .order_by(ToProfile.id.desc()).limit(20))).scalars().all()

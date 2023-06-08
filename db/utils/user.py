from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.user import UserNotifications
from datetime import datetime


async def add_user_notification(profile_id: int, user_id: int, is_request: bool, session: AsyncSession):
    req = UserNotifications(profile_id=profile_id, user_id=user_id, is_request=is_request)
    session.add(req)
    await session.commit()


async def get_user_notifications(user_id: int, session: AsyncSession):
    return (await session.execute(select(UserNotifications).filter(UserNotifications.user_id == user_id)
                                  .order_by(UserNotifications.id.desc())
                                  .limit(20))).scalars().all()


async def get_new_user_notifications(user_id: int, time: datetime, session: AsyncSession):
    return len((await session.execute(select(UserNotifications).filter(
        UserNotifications.user_id == user_id,
        UserNotifications.date > time
    ).order_by(UserNotifications.id.desc()).limit(20))).scalars().all())

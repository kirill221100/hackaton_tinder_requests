from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.profile import ProfileNotifications
from datetime import datetime


async def add_profile_notification(profile_id: int, user_id: int, is_request: bool, session: AsyncSession):
    req = ProfileNotifications(profile_id=profile_id, user_id=user_id, is_request=is_request)
    session.add(req)
    await session.commit()


async def get_profile_notifications(profile_id: int, session: AsyncSession):
    return (await session.execute(select(ProfileNotifications).filter(ProfileNotifications.profile_id == profile_id)
                                  .order_by(ProfileNotifications.id.desc()).limit(20))).scalars().all()


async def get_new_profile_notifications(profile_id: int, time: datetime, session: AsyncSession):
    return len((await session.execute(select(ProfileNotifications).filter(
        ProfileNotifications.profile_id == profile_id,
        ProfileNotifications.date > time
    ).order_by(ProfileNotifications.id.desc()).limit(20))).scalars().all())

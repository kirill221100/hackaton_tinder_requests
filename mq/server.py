import json
from sqlalchemy.ext.asyncio import AsyncSession
from db.utils.profile import add_profile_notification
from db.utils.user import add_user_notification
from aio_pika import connect_robust
from mq.ws import profile_manager, user_manager


async def srvr(session: AsyncSession) -> None:
    connection = await connect_robust(url="amqp://guest:guest@localhost/")
    queue_name = "test_queue"

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body.decode('utf-8'))
                    if data.get('to_user'):
                        await add_user_notification(data['profile_id'], data['user_id'], True, session)
                        await user_manager.send_personal_message(data)
                    else:
                        await add_profile_notification(data['profile_id'], data['user_id'], True, session)
                        await profile_manager.send_personal_message(data)


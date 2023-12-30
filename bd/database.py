import asyncpg
from aiogram import types


class Database:
    def __init__(self, pool):
        self.conn = None
        self.pool = pool

    async def create_pool(self, config):
        self.pool = await asyncpg.create_pool(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
        )
        self.conn = await self.pool.acquire()

    async def is_valid_channel_id(self, channel_id, bot):
        try:
            chat_info = await bot.get_chat(chat_id=channel_id)
            return chat_info.type == types.ChatType.CHANNEL
        except Exception as e:
            return False

    async def save_channel_to_db(self, channel_id, tg_channel):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO channels (vk_channel, tg_channel) VALUES ($1::bigint, $2::bigint) ON CONFLICT (vk_channel) DO UPDATE SET tg_channel = EXCLUDED.tg_channel;",
                channel_id, tg_channel,
            )

    async def take_group(self):
        query = "SELECT vk_channel FROM channels"
        groups = await self.conn.fetch(query)
        return [group['vk_channel'] for group in groups]

    async def take_channel(self, vk_channel):
        query = "SELECT tg_channel FROM channels WHERE vk_channel = $1"
        result = await self.conn.fetchval(query, vk_channel)
        return result

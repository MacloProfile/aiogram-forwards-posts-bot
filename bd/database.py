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
                "INSERT INTO channels (tg_channel, vk_channel) VALUES ($1::bigint, $2::bigint);",
                tg_channel, channel_id,
            )

    async def take_tg(self):
        query = "SELECT tg_channel FROM channels"
        result = await self.conn.fetchval(query)
        return result

    async def take_vk(self, tg_channel):
        query = "SELECT vk_channel FROM channels WHERE tg_channel = $1"
        results = await self.conn.fetch(query, tg_channel)
        return [result['vk_channel'] for result in results]

    async def check_channel_pair_exists(self, tg_channel_id, vk_channel_id):
        query = "SELECT COUNT(*) FROM channels WHERE tg_channel = $1 AND vk_channel = $2"
        count = await self.conn.fetchval(query, tg_channel_id, vk_channel_id)
        return count > 0

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

    async def save_user_to_db(self, user_id):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO users (user_id) VALUES ($1::bigint) ON CONFLICT (user_id) DO NOTHING;",
                user_id,
            )

    async def get_all_users(self):
        query = "SELECT * FROM users"
        results = await self.conn.fetch(query)
        return len(results)

    async def save_vk_token(self, user_id, token):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO tokens (user_id, token) VALUES ($1::bigint, $2::varchar) ON CONFLICT (user_id) DO UPDATE SET token = EXCLUDED.token RETURNING id;",
                user_id, token,
            )

    async def get_vk_token(self, user_id):
        query = "SELECT token FROM tokens WHERE user_id = $1"
        result = await self.conn.fetchval(query, user_id)
        return result
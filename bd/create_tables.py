import asyncpg


async def create_tables(pool):
    conn = await pool.acquire()

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id serial PRIMARY KEY,
            tg_channel bigint,
            vk_channel bigint
        );
    ''')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            user_id bigint UNIQUE
        );
    ''')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS tokens (
            id serial PRIMARY KEY,
            user_id bigint UNIQUE,
            token varchar
        );
    ''')

    await pool.release(conn)

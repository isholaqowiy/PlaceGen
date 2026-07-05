import aiosqlite
from config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                joined_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                dimensions TEXT,
                bg_color TEXT,
                text_content TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def register_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def save_placeholder_log(user_id: int, dimensions: str, bg_color: str, text_content: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO history (user_id, dimensions, bg_color, text_content) VALUES (?, ?, ?, ?)",
            (user_id, dimensions, bg_color, text_content)
        )
        await db.commit()

async def get_user_history(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT dimensions, bg_color, text_content FROM history WHERE user_id = ? ORDER BY id DESC LIMIT 5", (user_id,)) as cursor:
            return [{"dimensions": row[0], "bg_color": row[1], "text_content": row[2]} for row in await cursor.fetchall()]


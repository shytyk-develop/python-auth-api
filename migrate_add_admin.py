import asyncio

from sqlalchemy import text

from app.db.session import engine


async def migrate():
    """Add is_admin column to users table."""
    async with engine.begin() as conn:
        result = await conn.execute(
            text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name='users' AND column_name='is_admin'"
            )
        )
        if result.fetchone():
            print("✅ Column 'is_admin' already exists")
            return
        await conn.execute(
            text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT false")
        )
        print("✅ Column 'is_admin' added")


if __name__ == "__main__":
    asyncio.run(migrate())

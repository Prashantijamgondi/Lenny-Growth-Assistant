import asyncio
import asyncpg
import sys

# The Render connection string provided by the user
# Note: asyncpg prefers just 'postgres://' or 'postgresql://' 
DB_URL = "postgresql://custom_data_user:Al6FBhMjcks3c9xX83EVfE0A7oIbug4y@dpg-dactcqe7bikc73ffic90-a.singapore-postgres.render.com/custom_data"

async def main():
    print(f"Connecting to Render Database at {DB_URL.split('@')[1]}...")
    try:
        # Connect to the database
        conn = await asyncpg.connect(DB_URL)
        print("Successfully connected!")
        
        # Run the command to enable pgvector
        print("Enabling pgvector extension...")
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        print("Success! The 'vector' extension is now enabled.")
        
        await conn.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Windows specific fix for asyncio
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

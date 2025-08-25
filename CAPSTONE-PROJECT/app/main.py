from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

@app.get("/")
async def root():
    try:
        conn = psycopg2.connect(
            host="postgres-db",
            database=os.getenv("POSTGRES_DB", "mydb"),
            user=os.getenv("POSTGRES_USER", "myuser"),
            password=os.getenv("POSTGRES_PASSWORD", "mypassword"),
            cursor_factory=RealDictCursor
        )
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(50), email VARCHAR(100));")

        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) ON CONFLICT DO NOTHING;", 
                    ('Mohit', 'mohit@gmail.com'))
        
        cur.execute("SELECT * FROM users;")
        result = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Connected to Postgres!", "users": result}
    except Exception as e:
        return {"message": f"Error connecting to Postgres: {str(e)}"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
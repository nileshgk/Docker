
import os
import time
import mysql.connector

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Multi-Tier Application API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Demo only; restrict this in production.
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "database"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME", "appdb"),
    "user": os.getenv("DB_USER", "appuser"),
    "password": os.getenv("DB_PASSWORD", ""),
}

def get_connection():
    for attempt in range(10):
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error:
            if attempt == 9:
                raise
            time.sleep(3)

def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message VARCHAR(500) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()

@app.on_event("startup")
def startup():
    initialize_database()

class MessageRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/messages")
def get_messages():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, message, created_at FROM messages ORDER BY id DESC"
        )
        messages = cursor.fetchall()

        cursor.close()
        connection.close()

        for item in messages:
            item["created_at"] = item["created_at"].isoformat()

        return {"messages": messages}

    except mysql.connector.Error:
        raise HTTPException(status_code=503, detail="Database unavailable")

@app.post("/messages")
def create_message(request: MessageRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO messages (message) VALUES (%s)",
            (message,)
        )

        connection.commit()
        message_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return {"id": message_id, "message": message}

    except mysql.connector.Error:
        raise HTTPException(status_code=503, detail="Database unavailable")

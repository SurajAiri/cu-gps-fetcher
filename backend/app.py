import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="Forensic Location Tracking API")

# Enable CORS for the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/track")
async def track_client(request: Request):
    """
    Forensic Endpoint: Network-based Location Inference.
    Extracts the client's public IP and queries a geolocation database.
    """
    # In a production/viva environment, we use headers like X-Forwarded-For if behind a proxy
    client_ip = request.headers.get("x-forwarded-for") or request.client.host

    # Handle localhost/development cases
    if client_ip == "127.0.0.1" or client_ip == "::1":
        # For local testing, we query based on the external IP of the server
        api_url = "http://ip-api.com/json/"
    else:
        api_url = f"http://ip-api.com/json/{client_ip}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            data = response.json()

        if data.get("status") == "fail":
            return {"error": "Could not infer location from IP", "ip": client_ip}

        return {
            "latitude": data.get("lat"),
            "longitude": data.get("lon"),
            "city": data.get("city"),
            "country": data.get("country"),
            "isp": data.get("isp"),
            "ip": data.get("query"),
            "method": "Network-based (IP Geolocation)",
            "accuracy_note": "Approximate, ±5–10 km (ISP Node Level)",
            "forensic_confidence": "Medium",
            "mode": "Passive Inference",
        }
    except Exception as e:
        return {"error": str(e), "method": "None"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

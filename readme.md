# GPS Fetcher - Hybrid Location Tracking System

### Cyber Forensics Framework for Educational Purposes

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-Educational-red.svg)](#)

---

## ⚠️ LEGAL & ETHICAL DISCLAIMER

**IMPORTANT: This project is strictly for EDUCATIONAL AND ACADEMIC PURPOSES ONLY.**

This system was developed as a final-year assignment for the "Ethical Hacking & Cyber Forensics" course at Chandigarh University. The goal is to demonstrate:

- How geographic telemetry can be exfiltrated through social engineering
- Technical failover mechanisms in location tracking
- Security vulnerabilities in web-based location services

### Critical Legal Warnings:

- 🚫 **No Liability:** The author and developers are NOT responsible for any misuse, damage, or illegal activities conducted with this software
- 🔒 **Privacy:** Tracking individuals without explicit consent is **ILLEGAL** in most jurisdictions
- 📋 **Compliance:** This is a Proof of Concept (PoC) - **NOT for production or malicious use**
- ⚖️ **Usage:** Must only be used in controlled, authorized laboratory environments with proper consent

**By using this software, you acknowledge that you understand and will comply with all applicable laws and ethical guidelines.**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technical Stack](#technical-stack)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Security Features](#security-features)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Educational Insights](#educational-insights)

---

## 🎯 Overview

The **GPS Fetcher** is a hybrid location tracking system that demonstrates advanced concepts in cyber forensics and ethical hacking. It showcases a "Fail-Soft" architecture where location data is collected through multiple fallback mechanisms, simulating real-world attack scenarios for educational analysis.

### Key Concepts Demonstrated:

- **Social Engineering:** Deceptive user interface masquerading as a legitimate security tool
- **Hybrid Tracking:** GPS + IP-based geolocation with automatic failover
- **Secure Command & Control:** JWT-authenticated administrative dashboard
- **Forensic Data Collection:** Persistent logging with SQLite for evidence preservation

---

## ✨ Features

### 🎭 User Interface (Target Side)

- **Social Engineering Lure:** Disguised as "CloudShield Security Suite" integrity audit
- **Dual Tracking Methods:**
  - **Primary (Active):** High-precision HTML5 Geolocation API
  - **Secondary (Passive):** IP-based geolocation fallback via ip-api.com
- **Deception Mechanics:** Fake security report display to minimize target suspicion
- **Progressive Scanning UI:** Realistic scanning animation for authenticity

### 🛡️ Admin Dashboard (C2 Portal)

- **JWT Authentication:** Secure token-based access control
- **Real-time Telemetry:** Live tracking data with timestamps and location details
- **Interactive Map:** Leaflet.js visualization with OpenStreetMap tiles
- **Asset Management:** Toggle and focus on specific targets
- **Dark Mode Forensic UI:** Professional command center aesthetic
- **Comprehensive Logs:** Method used, accuracy, IP address, city/country data

### 🔐 Security Features

- JWT token-based authentication with 2-hour expiration
- Secure API endpoints with Bearer token validation
- CORS configured for controlled cross-origin access
- SQLite database for forensic evidence preservation
- Protected admin routes with dependency injection

---

## 🏗️ System Architecture

The framework implements a **Fail-Soft Hybrid Architecture**, ensuring location data is captured regardless of target device configuration or privacy settings.

```
┌─────────────────┐         ┌─────────────────┐         ┌──────────────────┐
│   User (Target) │◄───────►│  Backend Server │◄───────►│ Admin Dashboard  │
│   user.html     │   HTTP   │    app.py       │   JWT   │   admin.html     │
└─────────────────┘         └─────────────────┘         └──────────────────┘
        │                            │
        │ GPS/IP Data                │ SQLite
        ▼                            ▼
 ┌──────────────┐           ┌──────────────┐
 │ Geolocation  │           │ forensics.db │
 │    APIs      │           │   Database   │
 └──────────────┘           └──────────────┘
```

### Component Breakdown:

#### 1. **Backend Service** (`backend/app.py`)

- **Framework:** FastAPI (Python 3.x)
- **Server:** Uvicorn ASGI server
- **Authentication:** PyJWT for secure token generation and validation
- **Database:** SQLite3 for forensic data persistence
- **API Client:** HTTPX for async IP geolocation queries

**Key Endpoints:**

- `POST /login` - Admin authentication & JWT issuance
- `GET /track-ip` - Passive IP-based location lookup (public)
- `POST /log-target` - Location data ingestion (public)
- `GET /get-all-targets` - Protected forensic data retrieval (JWT required)

#### 2. **Target Interface** (`frontend/user.html`)

- **Purpose:** Social engineering lure for data collection
- **Design:** Professional security audit interface
- **Technology:** Vanilla JavaScript, Tailwind CSS
- **Tracking Logic:**
  - Attempts browser Geolocation API first
  - Falls back to IP geolocation on denial/timeout
  - Sends collected data to backend silently
  - Displays fake security report post-exfiltration

#### 3. **Admin Dashboard** (`frontend/admin.html`)

- **Purpose:** Secure command & control center
- **Authentication:** JWT-protected Single Page Application
- **Visualization:** Leaflet.js with inverted OpenStreetMap tiles
- **Features:**
  - Login portal with credential validation
  - Real-time target list with comprehensive metadata
  - Interactive map with marker clustering
  - Asset controller with auto-fit bounds
  - Dark mode terminal aesthetic

---

## 🛠️ Technical Stack

| Layer              | Technology                | Purpose                              |
| ------------------ | ------------------------- | ------------------------------------ |
| **Backend**        | Python 3.x                | Core application logic               |
| **Web Framework**  | FastAPI                   | High-performance async REST API      |
| **Server**         | Uvicorn                   | ASGI application server              |
| **Authentication** | PyJWT                     | JSON Web Token generation/validation |
| **HTTP Client**    | HTTPX                     | Async IP geolocation API requests    |
| **Database**       | SQLite3                   | Forensic data persistence            |
| **Frontend**       | Vanilla JavaScript (ES6+) | Client-side logic                    |
| **UI Framework**   | Tailwind CSS              | Responsive utility-first styling     |
| **Mapping**        | Leaflet.js                | Interactive map visualization        |
| **Map Tiles**      | OpenStreetMap             | Geographic tile rendering            |

---

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.x** (3.8 or higher recommended)
- **pip** (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for IP geolocation API)

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd gps-fetcher
```

### Step 2: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Or install manually:**

```bash
pip install fastapi uvicorn httpx pyjwt
```

### Step 3: Start Backend Server

```bash
cd backend
python app.py
```

**Expected Output:**

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

The server will automatically create `forensics.db` on first run.

### Step 4: Access Frontend Interfaces

**Option A - Local Testing:**

1. Open `frontend/user.html` in browser (simulates target)
2. Open `frontend/admin.html` in separate tab/window

**Option B - Remote Testing (Ngrok):**

```bash
# In a new terminal
ngrok http 8000
```

Then update the `API_BASE` variable in both HTML files:

```javascript
const API_BASE = "https://your-ngrok-url.ngrok.io";
```

### Default Admin Credentials

- **Username:** `admin`
- **Password:** `cyber123`

⚠️ **Change these in production environments!** Update in `backend/app.py`:

```python
ADMIN_USER = "admin"
ADMIN_PASS = "cyber123"
SECRET_KEY = "FORENSIC_SECRET_77"  # Change this!
```

---

## 📖 Usage Guide

### For Students/Researchers:

#### Testing Scenario 1: GPS-Enabled Device

1. Start backend server
2. Open `user.html` on a device with GPS (smartphone, laptop with location services)
3. Click "Run Security Audit"
4. **Allow** location permissions
5. Observe high-precision GPS coordinates logged
6. Check admin dashboard for real-time update

#### Testing Scenario 2: GPS-Denied Fallback

1. Open `user.html` on any device
2. Click "Run Security Audit"
3. **Deny** location permissions
4. Observe IP-based geolocation fallback
5. Check admin dashboard for approximate location

#### Testing Scenario 3: Admin Monitoring

1. Open `admin.html`
2. Login with credentials
3. View telemetry feed with:
   - Timestamp of capture
   - GPS vs IP method indicator
   - Accuracy level
   - IP address
   - City/Country approximation
4. Use map to visualize target locations
5. Export SQLite database for offline analysis

---

## 🔐 Security Features

### Authentication Flow

```
1. Admin enters credentials → 2. POST /login
3. Server validates → 4. JWT generated (2hr expiration)
5. Token stored in localStorage → 6. Attached to all API requests
7. Backend verifies token → 8. Access granted/denied
```

### JWT Token Structure

```json
{
  "sub": "admin",
  "exp": 1673456789
}
```

### Protected Routes

- `GET /get-all-targets` requires valid JWT
- Token must be sent as: `Authorization: Bearer <token>`
- Expired tokens automatically rejected

---

## 📁 Project Structure

```
gps-fetcher/
│
├── backend/
│   ├── app.py              # FastAPI application & routes
│   ├── requirements.txt    # Python dependencies
│   └── forensics.db        # SQLite database (auto-generated)
│
├── frontend/
│   ├── user.html          # Target interface (victim side)
│   └── admin.html         # Admin dashboard (C2 portal)
│
└── readme.md              # This file
```

---

## 📡 API Documentation

### Public Endpoints

#### `POST /login`

Authenticates admin user and issues JWT token.

**Request:**

```json
{
  "username": "admin",
  "password": "cyber123"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### `GET /track-ip`

Returns IP-based geolocation for requesting client.

**Response:**

```json
{
  "status": "success",
  "country": "India",
  "city": "Chandigarh",
  "lat": 30.7333,
  "lon": 76.7794,
  "query": "203.0.113.45"
}
```

#### `POST /log-target`

Logs captured location data to database.

**Request:**

```json
{
  "latitude": 30.7333,
  "longitude": 76.7794,
  "method": "GPS",
  "accuracy": "High",
  "city": "Chandigarh",
  "country": "India",
  "ip": "203.0.113.45"
}
```

### Protected Endpoints

#### `GET /get-all-targets`

Returns all tracked targets (requires JWT).

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response:**

```json
[
  {
    "id": 1,
    "latitude": 30.7333,
    "longitude": 76.7794,
    "method": "GPS",
    "accuracy": "High",
    "city": "Chandigarh",
    "country": "India",
    "ip": "203.0.113.45",
    "timestamp": "2026-01-11 14:30:22"
  }
]
```

---

## 🎓 Educational Insights

### For Academic Defense/Viva:

#### Key Discussion Points:

1. **Active vs Passive Tracking**

   - **Active (GPS):** Requires explicit user permission; provides high accuracy (±10-50m)
   - **Passive (IP):** Metadata-based; no permission needed; lower accuracy (city-level)
   - Demonstrates real-world attack vectors where fallback ensures data collection

2. **Social Engineering Techniques**

   - Interface mimics legitimate security software
   - Uses enterprise terminology ("integrity audit", "compliance check")
   - Displays fake reports to prevent user suspicion
   - Demonstrates importance of user awareness training

3. **JWT Authentication Security**

   - Prevents unauthorized access to sensitive forensic data
   - Token expiration (2 hours) limits exposure window
   - Demonstrates modern authentication patterns
   - Explain Bearer token scheme in headers

4. **Forensic Database Design**

   - SQLite chosen for portability and simplicity
   - Records complete "chain of custody" for geographic evidence
   - Timestamps ensure chronological integrity
   - Can be moved as single file for offline analysis

5. **Ethical Considerations**
   - Discuss consent requirements in real deployments
   - Legal implications of unauthorized tracking
   - Importance of responsible disclosure
   - Defensive measures users can implement

#### Common Viva Questions & Answers:

**Q: Why use SQLite instead of MySQL/PostgreSQL?**
A: SQLite is a single-file database perfect for forensic scenarios. The entire evidence trail can be copied, archived, and analyzed offline without server dependencies.

**Q: How would you defend against this attack?**
A: Browser location permission controls, VPN usage to mask IP, examining SSL certificates, user awareness training, and scrutinizing unexpected security prompts.

**Q: What's the difference between your GPS and IP tracking?**
A: GPS uses device hardware (satellites) for precise coordinates; IP geolocation uses network databases to approximate location based on ISP allocation, which is less accurate.

**Q: Is the JWT implementation production-ready?**
A: No - the secret key is hardcoded. Production systems should use environment variables, key rotation, refresh tokens, and HTTPS enforcement.

---

## 🔧 Troubleshooting

### Issue: Backend won't start

- Verify Python 3.x is installed: `python --version`
- Check if port 8000 is available
- Install missing dependencies: `pip install -r requirements.txt`

### Issue: Frontend can't connect to backend

- Ensure backend is running
- Check `API_BASE` URL in HTML files matches backend
- Verify CORS settings in `app.py`

### Issue: Location permission denied

- This is expected behavior - the IP fallback will activate
- Check browser console for permission errors
- Ensure HTTPS for production (browsers require secure context)

### Issue: JWT token expired

- Tokens last 2 hours by default
- Logout and login again to get fresh token
- Check system clock synchronization

---

## 📚 Further Learning

### Related Concepts:

- **OSINT (Open Source Intelligence):** Techniques for gathering publicly available information
- **Penetration Testing:** Ethical hacking methodologies and frameworks
- **Digital Forensics:** Evidence collection and analysis procedures
- **Web Security:** OWASP Top 10, CSP, CORS policies
- **Privacy Technologies:** VPNs, Tor, location spoofing

### Recommended Reading:

- OWASP Testing Guide
- "The Web Application Hacker's Handbook"
- NIST Cybersecurity Framework
- Local data protection laws (GDPR, CCPA, etc.)

---

## 📄 License

This project is for **educational purposes only**. No license is granted for commercial or malicious use.

---

## 👨‍💻 Author

**Semester 8 Student - Chandigarh University**  
Course: Ethical Hacking & Cyber Forensics  
Academic Year: 2025-2026

---

## 🙏 Acknowledgments

- FastAPI for excellent async web framework
- Leaflet.js for mapping capabilities
- OpenStreetMap contributors
- ip-api.com for geolocation services
- Tailwind CSS for UI components

---

**Remember: With great power comes great responsibility. Use this knowledge ethically and legally.**

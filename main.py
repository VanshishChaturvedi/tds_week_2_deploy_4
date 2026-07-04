from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from collections import defaultdict

app = FastAPI()

# 1. CORS Policy: Allow all (*) as requested
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Assigned API Key
ASSIGNED_API_KEY = "ak_f5mihybus8qb1o18anbgt51n"

# 3. Request Body Schemas
class Event(BaseModel):
    user: str
    amount: float
    ts: int

class AnalyticsPayload(BaseModel):
    events: List[Event]

# 4. Analytics Endpoint
@app.post("/analytics")
async def process_analytics(payload: AnalyticsPayload, x_api_key: Optional[str] = Header(None)):
    # Verify API Key
    if x_api_key != ASSIGNED_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing API Key")

    events = payload.events
    
    unique_users = set()
    total_revenue = 0.0
    user_positive_revenue = defaultdict(float)

    for event in events:
        unique_users.add(event.user)
        # Only aggregate revenue for positive amounts
        if event.amount > 0:
            total_revenue += event.amount
            user_positive_revenue[event.user] += event.amount

    # Find the top user based on positive revenue
    top_user = max(user_positive_revenue, key=user_positive_revenue.get) if user_positive_revenue else ""

    return {
        "email": "YOUR_LOGGED_IN_EMAIL@example.com",  # <-- UPDATE THIS
        "total_events": len(events),
        "unique_users": len(unique_users),
        "revenue": total_revenue,
        "top_user": top_user
    }

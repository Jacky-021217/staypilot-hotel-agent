"""StayPilot demo ticket API. Fictional data, single-tenant, local SQLite only.

This is a portfolio learning backend, NOT a production hotel system.
"""
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field

DB_PATH = Path(os.getenv("STAYPILOT_DB", "staypilot_demo.sqlite3"))
API_KEY = os.getenv("STAYPILOT_API_KEY")
if not API_KEY:
    raise RuntimeError("Set STAYPILOT_API_KEY before starting the server")

app = FastAPI(title="StayPilot Demo Ticket API", version="0.2.0")


def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("""CREATE TABLE IF NOT EXISTS tickets (
        ticket_id TEXT PRIMARY KEY,
        request_id TEXT UNIQUE NOT NULL,
        room_number TEXT NOT NULL,
        category TEXT NOT NULL,
        department TEXT NOT NULL,
        summary TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        priority TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""")
    con.commit()
    return con


def require_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

Category = Literal["housekeeping", "maintenance", "complaint"]
Status = Literal["open", "accepted", "in_progress", "completed", "cancelled"]
DEPT = {"housekeeping": "housekeeping", "maintenance": "engineering", "complaint": "front_desk_manager"}


class CreateTicket(BaseModel):
    request_id: str = Field(min_length=3, max_length=100, description="Unique idempotency key for the confirmed request")
    room_number: str = Field(min_length=2, max_length=8, pattern=r"^[0-9A-Za-z-]+$")
    category: Category
    summary: str = Field(min_length=3, max_length=500)
    quantity: int = Field(default=1, ge=1, le=20)
    priority: Literal["normal", "high"] = "normal"
    confirmed: bool = Field(description="Must be true only after explicit user confirmation")


class UpdateTicket(BaseModel):
    status: Status


@app.get("/health")
def health():
    return {"ok": True, "demo": True}


@app.post("/tickets", status_code=201, dependencies=[Depends(require_key)])
def create_ticket(data: CreateTicket):
    if not data.confirmed:
        raise HTTPException(status_code=400, detail="Explicit user confirmation required")
    with db() as con:
        existing = con.execute("SELECT * FROM tickets WHERE request_id=?", (data.request_id,)).fetchone()
        if existing:
            return dict(existing)  # retry is idempotent
        ticket_id = "WO-" + uuid.uuid4().hex[:8].upper()
        timestamp = datetime.now(timezone.utc).isoformat()
        con.execute("""INSERT INTO tickets
            (ticket_id,request_id,room_number,category,department,summary,quantity,priority,status,created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)""", (
            ticket_id, data.request_id, data.room_number, data.category, DEPT[data.category],
            data.summary, data.quantity, data.priority, "open", timestamp
        ))
        row = con.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,)).fetchone()
    return dict(row)


@app.get("/tickets", dependencies=[Depends(require_key)])
def list_tickets(limit: int = Query(default=20, ge=1, le=100)):
    """Small protected operations view for the portfolio demo."""
    with db() as con:
        rows = con.execute("SELECT * FROM tickets ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    return {"tickets": [dict(row) for row in rows], "count": len(rows)}


@app.get("/tickets/{ticket_id}", dependencies=[Depends(require_key)])
def get_ticket(ticket_id: str):
    with db() as con:
        row = con.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return dict(row)


@app.patch("/tickets/{ticket_id}", dependencies=[Depends(require_key)])
def update_ticket(ticket_id: str, data: UpdateTicket):
    with db() as con:
        row = con.execute("SELECT status FROM tickets WHERE ticket_id=?", (ticket_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Ticket not found")
        transitions = {
            "open": {"accepted", "cancelled"},
            "accepted": {"in_progress", "cancelled"},
            "in_progress": {"completed"},
            "completed": set(), "cancelled": set()
        }
        if data.status not in transitions[row["status"]]:
            raise HTTPException(status_code=409, detail=f"Invalid transition: {row['status']} -> {data.status}")
        con.execute("UPDATE tickets SET status=? WHERE ticket_id=?", (data.status, ticket_id))
        result = con.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,)).fetchone()
    return dict(result)

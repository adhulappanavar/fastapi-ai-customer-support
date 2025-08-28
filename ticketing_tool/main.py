#!/usr/bin/env python3
"""
FastAPI Ticketing System
Independent ticket management system with SQLite database
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uvicorn

from database import db

# Initialize FastAPI app
app = FastAPI(
    title="Ticket Management System",
    description="Independent ticketing system for customer support",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TicketCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10)
    user_id: int
    category_id: int
    priority_id: int
    tags: Optional[str] = ""

class TicketUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    category_id: Optional[int] = None
    priority_id: Optional[int] = None
    status_id: Optional[int] = None
    assigned_to: Optional[int] = None
    tags: Optional[str] = None

class TicketResponse(BaseModel):
    id: int
    ticket_number: str
    title: str
    description: str
    user_id: int
    user_username: str
    user_full_name: str
    category_id: int
    category_name: str
    priority_id: int
    priority_name: str
    priority_color: str
    status_id: int
    status_name: str
    status_color: str
    assigned_to: Optional[int]
    assigned_username: Optional[str]
    assigned_full_name: Optional[str]
    created_at: str
    updated_at: str
    resolved_at: Optional[str]
    due_date: Optional[str]
    tags: Optional[str]

class TicketStats(BaseModel):
    total_tickets: int
    open_tickets: int
    resolved_tickets: int
    critical_tickets: int
    tickets_by_category: List[Dict[str, Any]]
    tickets_by_priority: List[Dict[str, Any]]

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    sla_hours: int

class PriorityResponse(BaseModel):
    id: int
    name: str
    description: str
    sla_hours: int
    color: str

class StatusResponse(BaseModel):
    id: int
    name: str
    description: str
    color: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Ticket Management System API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Ticket endpoints
@app.get("/tickets", response_model=List[TicketResponse])
async def get_tickets(
    limit: int = Query(50, ge=1, le=100, description="Number of tickets to return"),
    offset: int = Query(0, ge=0, description="Number of tickets to skip"),
    status_id: Optional[int] = Query(None, description="Filter by status ID"),
    priority_id: Optional[int] = Query(None, description="Filter by priority ID"),
    category_id: Optional[int] = Query(None, description="Filter by category ID")
):
    """Get tickets with optional filtering"""
    try:
        tickets = db.get_tickets(
            limit=limit,
            offset=offset,
            status_id=status_id,
            priority_id=priority_id,
            category_id=category_id
        )
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving tickets: {str(e)}")

@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: int):
    """Get a specific ticket by ID"""
    try:
        ticket = db.get_ticket(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return ticket
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving ticket: {str(e)}")

@app.post("/tickets", response_model=Dict[str, Any])
async def create_ticket(ticket: TicketCreate):
    """Create a new ticket"""
    try:
        # Validate that user exists
        users = db.get_users()
        user_exists = any(u['id'] == ticket.user_id for u in users)
        if not user_exists:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        
        # Validate category
        categories = db.get_categories()
        category_exists = any(c['id'] == ticket.category_id for c in categories)
        if not category_exists:
            raise HTTPException(status_code=400, detail="Invalid category ID")
        
        # Validate priority
        priorities = db.get_priority_levels()
        priority_exists = any(p['id'] == ticket.priority_id for p in priorities)
        if not priority_exists:
            raise HTTPException(status_code=400, detail="Invalid priority ID")
        
        # Set initial status to "Open" (ID 1)
        ticket_data = ticket.dict()
        ticket_data['status_id'] = 1
        
        ticket_id = db.create_ticket(ticket_data)
        
        return {
            "message": "Ticket created successfully",
            "ticket_id": ticket_id,
            "ticket_number": f"TKT-{str(ticket_id).zfill(3)}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating ticket: {str(e)}")

@app.put("/tickets/{ticket_id}")
async def update_ticket(ticket_id: int, ticket_update: TicketUpdate, user_id: int = Query(..., description="ID of user making the update")):
    """Update an existing ticket"""
    try:
        # Validate that ticket exists
        existing_ticket = db.get_ticket(ticket_id)
        if not existing_ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        # Validate user exists
        users = db.get_users()
        user_exists = any(u['id'] == user_id for u in users)
        if not user_exists:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        
        # Validate category if provided
        if ticket_update.category_id:
            categories = db.get_categories()
            category_exists = any(c['id'] == ticket_update.category_id for c in categories)
            if not category_exists:
                raise HTTPException(status_code=400, detail="Invalid category ID")
        
        # Validate priority if provided
        if ticket_update.priority_id:
            priorities = db.get_priority_levels()
            priority_exists = any(p['id'] == ticket_update.priority_id for p in priorities)
            if not priority_exists:
                raise HTTPException(status_code=400, detail="Invalid priority ID")
        
        # Validate status if provided
        if ticket_update.status_id:
            statuses = db.get_statuses()
            status_exists = any(s['id'] == ticket_update.status_id for s in statuses)
            if not status_exists:
                raise HTTPException(status_code=400, detail="Invalid status ID")
        
        # Validate assigned_to if provided
        if ticket_update.assigned_to:
            assigned_user_exists = any(u['id'] == ticket_update.assigned_to for u in users)
            if not assigned_user_exists:
                raise HTTPException(status_code=400, detail="Invalid assigned user ID")
        
        # Remove None values
        update_data = {k: v for k, v in ticket_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        success = db.update_ticket(ticket_id, update_data, user_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update ticket")
        
        return {"message": "Ticket updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating ticket: {str(e)}")

# Reference data endpoints
@app.get("/categories", response_model=List[CategoryResponse])
async def get_categories():
    """Get all ticket categories"""
    try:
        return db.get_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving categories: {str(e)}")

@app.get("/priorities", response_model=List[PriorityResponse])
async def get_priorities():
    """Get all priority levels"""
    try:
        return db.get_priority_levels()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving priorities: {str(e)}")

@app.get("/statuses", response_model=List[StatusResponse])
async def get_statuses():
    """Get all ticket statuses"""
    try:
        return db.get_statuses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving statuses: {str(e)}")

@app.get("/users", response_model=List[UserResponse])
async def get_users():
    """Get all users"""
    try:
        return db.get_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {str(e)}")

# Statistics endpoint
@app.get("/stats", response_model=TicketStats)
async def get_ticket_stats():
    """Get ticket statistics and analytics"""
    try:
        return db.get_ticket_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving statistics: {str(e)}")

# Search endpoint
@app.get("/search")
async def search_tickets(
    query: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(20, ge=1, le=50, description="Number of results to return")
):
    """Search tickets by title, description, or tags"""
    try:
        # Simple search implementation - in production, consider using full-text search
        all_tickets = db.get_tickets(limit=1000)  # Get all tickets for search
        
        results = []
        query_lower = query.lower()
        
        for ticket in all_tickets:
            if (query_lower in ticket['title'].lower() or
                query_lower in ticket['description'].lower() or
                (ticket['tags'] and query_lower in ticket['tags'].lower())):
                results.append(ticket)
        
        return {
            "query": query,
            "total_results": len(results),
            "results": results[:limit]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching tickets: {str(e)}")

# Dashboard endpoint
@app.get("/dashboard")
async def get_dashboard():
    """Get dashboard data including stats and recent tickets"""
    try:
        stats = db.get_ticket_stats()
        recent_tickets = db.get_tickets(limit=10, offset=0)
        
        return {
            "stats": stats,
            "recent_tickets": recent_tickets,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving dashboard data: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Ticket Management System...")
    print("📊 Database initialized with sample data")
    print("🌐 API available at http://localhost:8000")
    print("📚 API documentation at http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

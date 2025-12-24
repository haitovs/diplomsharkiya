"""
Sharkiya Event Discovery - Data Models
Pydantic models for event data validation
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class EventCategory(str, Enum):
    """Event category enumeration."""
    MUSIC = "Music"
    TECH = "Tech"
    SPORTS = "Sports"
    FOOD = "Food"
    ART = "Art"
    MARKET = "Market"
    FILM = "Film"
    WELLNESS = "Wellness"
    BUSINESS = "Business"
    SCIENCE = "Science"
    KIDS = "Kids"
    TRAVEL = "Travel"
    COMMUNITY = "Community"


class EventCity(str, Enum):
    """Turkmenistan cities enumeration."""
    ASHGABAT = "Ashgabat"
    MARY = "Mary"
    TURKMENABAT = "Türkmenabat"
    DASHOGUZ = "Dashoguz"
    BALKANABAT = "Balkanabat"
    AWAZA = "Awaza"


class EventBase(BaseModel):
    """Base event model with common fields."""
    title: str = Field(..., min_length=3, max_length=100, description="Event title")
    category: str = Field(..., description="Event category")
    city: str = Field(..., description="City where event takes place")
    venue: str = Field(..., min_length=3, max_length=200, description="Venue name and address")
    date_start: datetime = Field(..., description="Event start date and time")
    date_end: datetime = Field(..., description="Event end date and time")
    price: float = Field(default=0, ge=0, le=10000, description="Ticket price in TMT")
    popularity: int = Field(default=50, ge=1, le=100, description="Popularity score 1-100")
    lat: Optional[float] = Field(default=None, ge=35, le=43, description="Latitude")
    lon: Optional[float] = Field(default=None, ge=52, le=67, description="Longitude")
    image: Optional[str] = Field(default="", description="Image URL or path")
    description: str = Field(default="", max_length=2000, description="Event description")
    
    @field_validator('date_end')
    @classmethod
    def end_after_start(cls, v, info):
        if 'date_start' in info.data and v < info.data['date_start']:
            raise ValueError('End date must be after start date')
        return v
    
    @field_validator('category')
    @classmethod
    def valid_category(cls, v):
        valid = [c.value for c in EventCategory]
        if v not in valid:
            raise ValueError(f'Category must be one of: {", ".join(valid)}')
        return v


class EventCreate(EventBase):
    """Model for creating a new event."""
    pass


class EventUpdate(BaseModel):
    """Model for updating an event (all fields optional)."""
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    category: Optional[str] = None
    city: Optional[str] = None
    venue: Optional[str] = Field(None, min_length=3, max_length=200)
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    price: Optional[float] = Field(None, ge=0, le=10000)
    popularity: Optional[int] = Field(None, ge=1, le=100)
    lat: Optional[float] = Field(None, ge=35, le=43)
    lon: Optional[float] = Field(None, ge=52, le=67)
    image: Optional[str] = None
    description: Optional[str] = Field(None, max_length=2000)


class Event(EventBase):
    """Full event model with ID and metadata."""
    id: str = Field(..., description="Unique event identifier")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)
    
    # Computed fields (not stored)
    distance_km: Optional[float] = Field(default=None, description="Distance from search center")
    
    class Config:
        from_attributes = True


class EventFilters(BaseModel):
    """Model for event filtering parameters."""
    city: Optional[str] = None
    categories: Optional[List[str]] = None
    date_preset: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    search_query: Optional[str] = None
    center_lat: Optional[float] = None
    center_lon: Optional[float] = None
    radius_km: Optional[float] = None
    sort_by: Optional[str] = "Date (Soonest)"
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)


class Admin(BaseModel):
    """Admin user model."""
    id: Optional[int] = None
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[str] = None
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None


class AdminLogin(BaseModel):
    """Admin login credentials."""
    username: str
    password: str


class ImportResult(BaseModel):
    """Result of bulk import operation."""
    total: int = 0
    success: int = 0
    failed: int = 0
    errors: List[str] = Field(default_factory=list)


class Analytics(BaseModel):
    """Event analytics model."""
    event_id: str
    action: str  # 'view', 'save', 'share', 'directions'
    timestamp: datetime = Field(default_factory=datetime.now)

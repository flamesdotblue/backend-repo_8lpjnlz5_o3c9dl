"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogpost" collection
"""

from pydantic import BaseModel, Field
from typing import List, Optional

# ------------------------------
# Domain schemas for this project
# ------------------------------

class NewsItem(BaseModel):
    """
    News collection schema
    Collection name: "newsitem"
    """
    title: str = Field(..., description="Headline title")
    source: str = Field(..., description="News source/publication")
    category: str = Field(..., description="Category or sector tag")
    time: str = Field(..., description="Published time string, e.g., '7:35 AM'")
    tickers: List[str] = Field(default_factory=list, description="Related tickers, e.g., ['RELIANCE']")

class StockRecommendation(BaseModel):
    """
    Stock recommendations schema
    Collection name: "stockrecommendation"
    """
    company: str = Field(..., description="Company name")
    ticker: str = Field(..., description="Ticker symbol")
    sector: str = Field(..., description="Sector name")
    risk: str = Field(..., description="Risk level: Low/Medium/High")
    bias: str = Field(..., description="Bias: Long/Short")
    sentiment: str = Field(..., description="Sentiment: Bullish/Bearish/Neutral")
    rationale: str = Field(..., description="Brief rationale for the call")
    signals: List[str] = Field(default_factory=list, description="Bullet points behind the call")
    keywords: List[str] = Field(default_factory=list, description="Keywords for search/filtering")

# Example schemas (kept for reference)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True

import os
from datetime import datetime
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import NewsItem, StockRecommendation

app = FastAPI(title="Pre-Market India API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Pre-Market India API running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        from database import db

        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except ImportError:
        response["database"] = "❌ Database module not found"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response


# In a future iteration, these would be powered by crawlers and filings parsers
# For now, we serve structured, curated examples so the UI is functional end-to-end


def sample_news() -> List[NewsItem]:
    now = datetime.now().replace(second=0, microsecond=0)
    def ts(minutes_ago: int) -> str:
        t = now.replace()  # copy
        return (now).strftime("%I:%M %p").lstrip('0')

    return [
        NewsItem(
            title="Oil prices steady; OMCs watch margins into open",
            source="Business Standard",
            category="Commodities",
            time="7:42 AM",
            tickers=["RELIANCE", "IOC", "BPCL", "HPCL"],
        ),
        NewsItem(
            title="IT services signal improving deal pipeline in Q3 commentary",
            source="ET Markets",
            category="Technology",
            time="7:35 AM",
            tickers=["TCS", "INFY", "WIPRO"],
        ),
        NewsItem(
            title="Banking liquidity eases; deposit growth stabilises",
            source="Mint",
            category="Banking",
            time="7:20 AM",
            tickers=["HDFCBANK", "ICICIBANK", "SBIN"],
        ),
        NewsItem(
            title="US launches support pharma exporters; specialty pipeline updates",
            source="Financial Express",
            category="Healthcare",
            time="7:05 AM",
            tickers=["SUNPHARMA", "DRREDDY", "CIPLA"],
        ),
    ]


def sample_recommendations() -> List[StockRecommendation]:
    return [
        StockRecommendation(
            company="Reliance Industries",
            ticker="RELIANCE",
            sector="Energy",
            risk="Medium",
            bias="Long",
            sentiment="Bullish",
            rationale=(
                "Retail and telecom momentum alongside steady energy margins. "
                "Recent partnership updates support growth narrative."
            ),
            signals=[
                "Retail expansion and subscriber additions",
                "Stable GRMs; energy complex supportive",
                "Diversified revenue streams",
            ],
            keywords=["Retail", "Telecom", "Margins"],
        ),
        StockRecommendation(
            company="Tata Consultancy Services",
            ticker="TCS",
            sector="IT",
            risk="Low",
            bias="Long",
            sentiment="Neutral",
            rationale=(
                "Muted near-term outlook priced in; improving deal pipeline and currency tailwinds could aid open."
            ),
            signals=[
                "Large deal wins commentary",
                "INR tailwind vs USD",
                "Valuation support",
            ],
            keywords=["Orderbook", "Currency", "Valuation"],
        ),
        StockRecommendation(
            company="HDFC Bank",
            ticker="HDFCBANK",
            sector="Banking",
            risk="Medium",
            bias="Long",
            sentiment="Bullish",
            rationale=(
                "Deposit growth and NIM stabilisation improves sentiment ahead of session."
            ),
            signals=[
                "Deposit growth commentary",
                "Stable asset quality",
                "Supportive liquidity",
            ],
            keywords=["NIM", "Deposits", "Asset Quality"],
        ),
        StockRecommendation(
            company="Zee Entertainment",
            ticker="ZEEL",
            sector="Media",
            risk="High",
            bias="Short",
            sentiment="Bearish",
            rationale=(
                "Merger overhang and regulatory uncertainty could weigh on open; headline risk elevated."
            ),
            signals=[
                "Merger timeline questions",
                "Pending regulatory clarity",
                "Elevated volatility",
            ],
            keywords=["Merger", "Regulatory", "Volatility"],
        ),
        StockRecommendation(
            company="Sun Pharma",
            ticker="SUNPHARMA",
            sector="Pharma",
            risk="Low",
            bias="Long",
            sentiment="Bullish",
            rationale=(
                "Favorable update on specialty pipeline and US market traction; defensives in favour pre-open."
            ),
            signals=[
                "US pipeline progress",
                "Specialty portfolio momentum",
                "Healthcare rotation",
            ],
            keywords=["Specialty", "US Markets", "Defensive"],
        ),
    ]


@app.get("/api/news", response_model=List[NewsItem])
def get_news():
    items = sample_news()
    # Optional: store snapshot if DB available
    try:
        from database import db, create_document
        if db is not None:
            for n in items:
                try:
                    create_document("newsitem", n)
                except Exception:
                    pass
    except Exception:
        pass
    return items


@app.get("/api/recommendations", response_model=List[StockRecommendation])
def get_recommendations():
    recs = sample_recommendations()
    # Optional: store snapshot if DB available
    try:
        from database import db, create_document
        if db is not None:
            for r in recs:
                try:
                    create_document("stockrecommendation", r)
                except Exception:
                    pass
    except Exception:
        pass
    return recs


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

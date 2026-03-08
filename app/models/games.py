from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional

class GamePrice(BaseModel):
    game_id: str
    store: str
    price: float
    currency: str = "USD"
    url: Optional[str] = None


class PriceComparison(BaseModel):
    store: str
    price: float
    url: Optional[str] = None


class GameResponse(BaseModel):
    id: str
    title: str
    description: str
    image: str
    originalPrice: float
    currentPrice: float
    discount: float
    genres: list[str]
    isTrending: bool
    isDealOfDay: bool
    priceComparison: Optional[list[PriceComparison]] = None

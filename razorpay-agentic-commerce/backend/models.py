from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class VoiceCommandIn(BaseModel):
    user_id: int = 1
    text: str


class SpendLimitIn(BaseModel):
    user_id: int = 1
    limit: float


class PasskeyIn(BaseModel):
    user_id: int = 1


class BroadcastIn(BaseModel):
    intent_id: int


class HaggleIn(BaseModel):
    intent_id: int
    bid: Dict[str, Any]


class SyndicateIn(BaseModel):
    deal_id: int


class CheckoutIn(BaseModel):
    deal_id: int
    include_syndicate: bool = False


class DisputeIn(BaseModel):
    order_id: int
    reason: str
    delivered_desc: str
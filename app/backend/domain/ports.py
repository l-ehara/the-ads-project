from typing import Iterable, Protocol
from dataclasses import dataclass
from datetime import date

@dataclass
class AdsMetricDaily:
    date: date
    source: str
    account_id: str
    campaign_id: str
    adgroup_id: str | None
    ad_id: str | None
    impressions: int
    clicks: int
    spend: float
    conversions: float | None = None

class AdsConnector(Protocol):
    source: str
    async def fetch_daily(self, account_id: str, start: date, end: date) -> Iterable[AdsMetricDaily]: ...

class WarehouseWriter(Protocol):
    async def write_metrics(self, rows: Iterable[AdsMetricDaily]): ...

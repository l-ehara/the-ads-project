import csv
from datetime import date
from typing import Iterable
from app.backend.domain.ports import AdsConnector, AdsMetricDaily 

class GoogleAdsCSVMock(AdsConnector):
    source = "google_ads"

    def __init__(self, path: str):
        self.path = path

    async def fetch_daily(self, account_id: str, start: date, end: date) -> Iterable[AdsMetricDaily]:
        with open(self.path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                d = date.fromisoformat(row["date"])
                if not (start <= d <= end):
                    continue
                yield AdsMetricDaily(
                    date=d,
                    source=self.source,
                    account_id=account_id,
                    campaign_id=row["campaign_id"],
                    adgroup_id=row.get("adgroup_id"),
                    ad_id=row.get("ad_id"),
                    impressions=int(row["impressions"]),
                    clicks=int(row["clicks"]),
                    spend=float(row["spend"]),
                    conversions=float(row.get("conversions") or 0.0),
                )
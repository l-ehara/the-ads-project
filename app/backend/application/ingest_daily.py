from datetime import date
from typing import Iterable
from app.backend.domain.ports import AdsConnector, AdsMetricDaily, WarehouseWriter  # << absoluto

async def ingest_daily(connector: AdsConnector, writer: WarehouseWriter,
                       account_id: str, start: date, end: date) -> dict:
    rows: list[AdsMetricDaily] = [r async for r in connector.fetch_daily(account_id, start, end)]
    if rows:
        await writer.write_metrics(rows)
    total_spend = sum(r.spend for r in rows)
    return {"rows": len(rows), "spend": total_spend}
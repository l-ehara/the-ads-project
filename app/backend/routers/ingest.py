from fastapi import APIRouter, Query
from datetime import date
from app.backend.application.ingest_daily import ingest_daily
from app.backend.adapters.connectors.mocks.google_csv import GoogleAdsCSVMock
from app.backend.adapters.warehouse.local_parquet import LocalParquetWriter

router = APIRouter(prefix="/v1/ingest", tags=["ingest"])

@router.post("/{source}")
async def ingest(source: str,
                account_id: str = Query("test-account"),
                since: date = Query(...), until: date = Query(...)):
    if source == "google":
        connector = GoogleAdsCSVMock(path="app/backend/tests/data/google_sample.csv")
    else:
        return {"error": f"source '{source}' ainda não suportada no mock"}
    writer = LocalParquetWriter(base_dir=".data")
    result = await ingest_daily(connector, writer, account_id, since, until)
    return result

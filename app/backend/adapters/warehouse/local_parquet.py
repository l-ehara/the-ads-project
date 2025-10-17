import os
import pandas as pd
from typing import Iterable
from app.backend.domain.ports import AdsMetricDaily, WarehouseWriter  # << absoluto

class LocalParquetWriter(WarehouseWriter):
    def __init__(self, base_dir: str = ".data"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    async def write_metrics(self, rows: Iterable[AdsMetricDaily]):
        data = [r.__dict__ for r in rows]
        if not data:
            return 0
        df = pd.DataFrame(data)
        path = os.path.join(self.base_dir, f"{df.source.iloc[0]}_metrics.parquet")
        df.to_parquet(path, index=False)
        return len(df)
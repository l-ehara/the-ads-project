import os
from datetime import date
import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ads Insights", layout="wide")
st.title("Ads Insights — Frontend (MVP)")

# Backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
st.caption(f"Backend: {BACKEND_URL}")

with st.sidebar:
    st.header("Ingestão (Google - mock CSV)")
    since = st.date_input("Desde", value=date(2025, 10, 1))
    until = st.date_input("Até", value=date(2025, 10, 3))
    run_ingest = st.button("Rodar ingestão")

# Ação: chamar ingestão no backend
if run_ingest:
    try:
        url = f"{BACKEND_URL}/v1/ingest/google"
        params = {"since": since.isoformat(), "until": until.isoformat()}
        r = requests.post(url, params=params, timeout=60)
        r.raise_for_status()
        st.success("Ingestão executada com sucesso!")
        st.json(r.json())
    except Exception as e:
        st.error(f"Falha ao chamar o backend: {e}")

st.divider()
st.subheader("KPIs")

# Carrega o parquet gerado pelo backend (writer local)
parquet_path = "app/.data/google_ads_metrics.parquet"
if os.path.exists(parquet_path):
    df = pd.read_parquet(parquet_path)
    if not df.empty:
        # Normalizações e KPIs
        if "impressions" in df and "clicks" in df:
            df["ctr"] = (df["clicks"] / df["impressions"]).fillna(0.0)
        if "clicks" in df and "spend" in df:
            df["cpc"] = (df["spend"] / df["clicks"]).replace([pd.NA, pd.NaT], 0).fillna(0.0)
        if "impressions" in df and "spend" in df:
            df["cpm"] = (df["spend"] / df["impressions"] * 1000).fillna(0.0)

        # Tabela
        st.dataframe(df.sort_values("date").reset_index(drop=True))

        # Gráficos simples
        kpi_cols = st.columns(4)
        kpi_cols[0].metric("Spend total", f"{df['spend'].sum():.2f}")
        kpi_cols[1].metric("Impressions", int(df["impressions"].sum()))
        kpi_cols[2].metric("Clicks", int(df["clicks"].sum()))
        kpi_cols[3].metric("CTR médio", f"{df['ctr'].mean()*100:.2f}%")

        st.subheader("Spend por dia")
        st.line_chart(df.groupby("date", as_index=False)["spend"].sum(), x="date", y="spend")

        st.subheader("Top campanhas por spend")
        top_campaigns = (
            df.groupby("campaign_id", as_index=False)["spend"].sum()
            .sort_values("spend", ascending=False).head(10)
        )
        st.bar_chart(top_campaigns, x="campaign_id", y="spend")
    else:
        st.info("Ainda não há linhas no Parquet. Rode a ingestão na barra lateral.")
else:
    st.info("Arquivo app/.data/google_ads_metrics.parquet não encontrado. Rode a ingestão primeiro.")
import streamlit as st
import os
import sys
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

st.set_page_config(page_title="Freshdesk AI Analytics", page_icon="📊", layout="wide")

if "pipeline" not in st.session_state:
    st.session_state.pipeline = None
    st.session_state.log = ""
    st.session_state.error = None
    st.session_state.fetched_df = None

st.title("📊 Freshdesk AI Analytics")
st.caption("v1.0 · Analyze tickets locally")

# Load stored Freshdesk credentials
try:
    from load_config import load_freshdesk_config
    fd_domain, fd_api_key = load_freshdesk_config()
except:
    fd_domain = os.environ.get("FRESHDESK_DOMAIN", "")
    fd_api_key = os.environ.get("FRESHDESK_API_KEY", "")

with st.sidebar:
    st.header("1. Get Tickets")
    
    source = st.radio("Source", ["Upload file", "Fetch from Freshdesk"], label_visibility="collapsed")
    
    uploaded = None
    if source == "Upload file":
        uploaded = st.file_uploader("Upload Freshdesk export", type=["csv", "xlsx"])
    else:
        st.info(f"📌 Using stored credentials from config.yaml")
        fetch_btn = st.button("🔄 Fetch from Freshdesk", type="primary", use_container_width=True)
        
        if fetch_btn:
            if not fd_domain or not fd_api_key:
                st.error("❌ Freshdesk credentials not found in config.yaml")
                st.stop()
            
            with st.spinner("Fetching tickets from Freshdesk..."):
                try:
                    from freshdesk_client import FreshdeskClient
                    client = FreshdeskClient(domain=fd_domain, api_key=fd_api_key)
                    df = client.fetch_dataframe(max_pages=5, per_page=100)
                    st.session_state.fetched_df = df
                    st.success(f"✅ Fetched {len(df):,} tickets")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    st.divider()
    st.header("2. AI Settings")
    if "anthropic_api_key" not in st.session_state:
        st.session_state.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    st.text_input("Anthropic API Key", key="anthropic_api_key", type="password", help="Optional: for AI classification")
    
    st.divider()
    st.header("3. Analyze")
    can_run = uploaded is not None or st.session_state.fetched_df is not None
    run_btn = st.button("🚀 Run Analysis", type="primary", use_container_width=True, disabled=not can_run)

# Run analysis
if run_btn:
    try:
        INPUT_DIR = ROOT_DIR / "input"
        INPUT_DIR.mkdir(exist_ok=True)
        
        # Determine input
        if uploaded:
            input_path = INPUT_DIR / uploaded.name
            input_path.write_bytes(uploaded.getvalue())
        elif st.session_state.fetched_df is not None:
            input_path = INPUT_DIR / "freshdesk_fetched.csv"
            st.session_state.fetched_df.to_csv(input_path, index=False)
        else:
            st.error("No input selected")
            st.stop()
        
        with st.spinner("Running analysis pipeline..."):
            if st.session_state.anthropic_api_key:
                os.environ["ANTHROPIC_API_KEY"] = st.session_state.anthropic_api_key
            
            from pipeline import SupportIntelligencePipeline
            pipeline = SupportIntelligencePipeline(str(input_path))
            pipeline.run()
            st.session_state.pipeline = pipeline
        
        st.success(f"✅ Analysis complete! {len(pipeline.master_df):,} tickets processed.")
    except Exception as e:
        st.error(f"Error: {e}")

# Results
if st.session_state.pipeline:
    pipeline = st.session_state.pipeline
    
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📊 Full Data", "⬇️ Download"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        col1.metric("Tickets", len(pipeline.master_df))
        col2.metric("Products", pipeline.master_df["Product"].nunique() if "Product" in pipeline.master_df.columns else 0)
        col3.metric("Categories", pipeline.master_df["Category"].nunique() if "Category" in pipeline.master_df.columns else 0)
        
        if "Product" in pipeline.master_df.columns:
            st.subheader("Top Products")
            st.bar_chart(pipeline.master_df["Product"].value_counts().head(10))
        
        if "Sentiment" in pipeline.master_df.columns:
            st.subheader("Sentiment Distribution")
            st.bar_chart(pipeline.master_df["Sentiment"].value_counts())
    
    with tab2:
        st.dataframe(pipeline.master_df, use_container_width=True)
    
    with tab3:
        st.subheader("Generated Reports")
        OUTPUT_DIR = ROOT_DIR / "output"
        files = sorted(OUTPUT_DIR.glob("*.xlsx"), key=lambda p: p.stat().st_mtime, reverse=True)
        
        for f in files[:5]:
            with open(f, "rb") as file:
                st.download_button(
                    label=f"📥 {f.name}",
                    data=file.read(),
                    file_name=f.name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
else:
    st.info("👆 Upload a file or fetch from Freshdesk to get started")

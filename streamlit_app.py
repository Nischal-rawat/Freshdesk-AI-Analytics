"""
Freshdesk AI Analytics — Customer Success Tools
Support Intelligence Platform with AI-powered modules
"""

import contextlib
import io
import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Ensure UTF-8 encoding
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

try:
    from config import APP_NAME, VERSION, INPUT_DIR, OUTPUT_DIR
except ImportError:
    APP_NAME = "Freshdesk AI Analytics"
    VERSION = "1.0"
    INPUT_DIR = ROOT_DIR / "input"
    OUTPUT_DIR = ROOT_DIR / "output"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📊",
    layout="wide",
)

if "pipeline" not in st.session_state:
    st.session_state.pipeline = None
    st.session_state.log = ""
    st.session_state.error = None

st.title(f"📊 {APP_NAME}")
st.caption(f"v1.0 · AI-powered customer success tools")

with st.sidebar:
    st.header("Configuration")
    
    if "anthropic_api_key" not in st.session_state:
        st.session_state.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    
    st.subheader("1. Input Data")
    
    INPUT_DIR = ROOT_DIR / "input"
    INPUT_DIR.mkdir(exist_ok=True)
    
    source = st.radio("Ticket source", ["Upload file", "Use sample file"], label_visibility="collapsed")
    
    uploaded_file = None
    if source == "Upload file":
        uploaded_file = st.file_uploader("Upload Freshdesk export", type=["csv", "xlsx"])
    
    st.divider()
    st.subheader("2. AI Settings")
    
    use_ai = st.checkbox("Use Claude AI", value=False)
    if use_ai:
        st.text_input("Anthropic API Key", key="anthropic_api_key", type="password")
    
    st.divider()
    can_run = uploaded_file is not None or source == "Use sample file"
    run_button = st.button("🚀 Run Analysis", type="primary", use_container_width=True, disabled=not can_run)

if run_button:
    try:
        if source == "Upload file" and uploaded_file:
            input_path = INPUT_DIR / uploaded_file.name
            input_path.write_bytes(uploaded_file.getvalue())
        else:
            st.info("Using sample data...")
            input_path = None
        
        with st.spinner("Running analysis..."):
            if use_ai and st.session_state.anthropic_api_key:
                os.environ["ANTHROPIC_API_KEY"] = st.session_state.anthropic_api_key
            
            from pipeline import SupportIntelligencePipeline
            pipeline = SupportIntelligencePipeline(str(input_path))
            pipeline.run()
            st.session_state.pipeline = pipeline
        
        st.success(f"✅ Complete! Processed {len(pipeline.master_df):,} tickets.")
    
    except Exception as e:
        st.error(f"❌ Error: {e}")

if st.session_state.pipeline:
    pipeline = st.session_state.pipeline
    
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Data", "📚 Tools"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        col1.metric("Tickets", len(pipeline.master_df))
        col2.metric("Products", pipeline.master_df["Product"].nunique() if "Product" in pipeline.master_df.columns else 0)
        col3.metric("Categories", pipeline.master_df["Category"].nunique() if "Category" in pipeline.master_df.columns else 0)
        
        if "Product" in pipeline.master_df.columns:
            st.bar_chart(pipeline.master_df["Product"].value_counts().head(10))
    
    with tab2:
        st.dataframe(pipeline.master_df, use_container_width=True)
    
    with tab3:
        st.info("✉️ Reply Drafter | 📧 Mail Generator | 🗺️ Plans | 📘 Playbooks\n\n(Coming soon)")
else:
    st.info("👆 Upload a file and click Run to get started.")

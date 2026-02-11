import streamlit as st
import pandas as pd
import io

# 1. 페이지 설정 및 다크 테마
st.set_page_config(page_title="일일 재고현황 시스템", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-layout {
        position: relative;
        width: 90%;
        margin: 50px auto;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    /* 격자 배경 */
    .grid-bg {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        grid-template-rows: repeat(2, 200px);
        width: 100%;
        border: 1px solid #3e4452;
        background-color: #1a1c24;
        position: relative;
    }
    .grid-item { border: 1px solid #2d3139; position: relative; }
    
    /* 공통 노드 스타일 */
    .node-base {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        z-index: 20;
    }
    /* 원형 노드 (교차점) */
    .node-circle {
        position: absolute;
        width: 85px; height: 85px;
        background: radial-gradient(circle, #2c3e50 0%, #000000 100%);
        border: 3px solid #00d4ff;
        border-radius: 50%;
        transform: translate(-50%, -50%);
        box-shadow: 0px 0px 12px rgba(0, 212, 255, 0.6);
    }
    /* 사각형 노드 (그리드 내부) */
    .node-square {
        width: 90%; height: 80%;
        background-color: #262a33;
        border: 2px solid #ffeb3b;
        margin: auto;
    }
    .addr { font-size: 11px; font-weight: bold; color: #ffffff; }
    .grain { font-size: 9px; color: #00d4ff; }
    .qty { font-size: 12px; font-weight: bold; color: #ffeb3b; }
    .node-off { border: 1px dashed #444 !important; background: transparent !important; color: #444 !important; box-shadow: none !important; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 일일 장치장별 & 곡종별 재고현황")

# 2. 데이터 입력 및 콤마 처리
raw_data = st.sidebar.text_area("데이터 입력 (주소 곡종 재고량)", height=400)
data_dict = {}
if raw_data.strip():
    for line in raw_data.strip().split('\n'):
        parts = line.split
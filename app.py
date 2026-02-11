import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고현황 시스템", layout="wide")

# CSS: 다크 테마 및 레벨 게이지 시각화
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .grid-wrapper { position: relative; width: 100%; margin-top: 60px; display: flex; flex-direction: column; }
    .grid-bg {
        display: grid; grid-template-columns: repeat(7, 1fr);
        grid-template-rows: repeat(2, 200px);
        width: 100%; border: 1px solid #3e4452; background-color: #1a1c24; position: relative;
    }
    .grid-item { border: 1px solid #2d3139; display: flex; align-items: center; justify-content: center; position: relative; }
    .node-base { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 10; overflow: hidden; }
    .circle {
        position: absolute; width: 85px; height: 85px;
        background-color: #000; border: 3px solid #00d4ff; border-radius: 50%;
        transform: translate(-50%, -50%); box-shadow: 0px 0px 10px rgba(0, 212, 255, 0.4);
    }
    .square { width: 90%; height: 85%; background-color: #000; border: 2px solid #ffeb3b; }
    .gauge-fill {
        position: absolute; bottom: 0; left: 0; width: 100%; 
        background-color: rgba(200, 200, 200, 0.2);
        z-index: -1;
    }
    .addr { font-size: 10px; font-weight: bold; color: #ffffff; z-index: 2; }
    .grain-txt { font-size: 8px; color: #00d4ff; z-index: 2; }
    .qty-txt { font-size: 11px; font-weight: bold; color: #ffeb3b; z-index: 2; }
    .off { border: 1px dashed #444 !important; background: transparent !important; color: #444 !important; }
    .summary-card {
        background-color: #1a1c24; border: 1px solid #3e4452;
        padding: 8px 12px; border-radius: 4px; margin-bottom: 6px;
        border-left: 3px solid #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 일일 장치장별 & 곡종별 재고현황")

# 2. 데이터 처리
st.sidebar.markdown("### 📋 데이터 입력")
raw_data = st.sidebar.text_area("주소 곡종 재고량", height=300)
data_dict = {}
summary_dict = {}

if raw_data.strip():
    for line in raw_data.strip().split('\n'):
        p = line.split()
        if len(p) >= 3:
            try:
                addr, grain, qty_str = p[0], p[1], p[2].replace(',', '')
                qty = float(qty_str)
                data_dict[addr] = {"g": grain, "q": qty}
                summary_dict[grain] = summary_dict.get(grain, 0) + qty
            except: continue

# 3. 화면 분할
col_left, col_right = st.columns([8, 2])

with col_left:
    st.subheader("📍 실시간 재고 레벨 맵")
    def draw_node(addr, is_circle=True, x=0, y=0):
        val = data_dict.get(addr)
        cls = "circle" if is_circle else "square"
        max_cap = 500 if is_circle else 2000
        pos = f"left:{x}%; top:{y}%;" if is_circle else ""
        if val:
            percent = min(100, (val['
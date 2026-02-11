import streamlit as st
import pandas as pd
import io

# 1. 페이지 설정
st.set_page_config(page_title="공정별 재고현황 시스템", layout="wide")

# 고사양 산업용 UI CSS
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-container {
        position: relative;
        width: 90%;
        margin: 50px auto;
        background-color: #1a1c24;
        border: 2px solid #3e4452;
        padding: 40px 0;
        display: flex;
        flex-direction: column;
        gap: 80px; /* 행 간격 */
    }
    .row {
        position: relative;
        width: 100%;
        height: 100px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    /* 7개 사각형 그리드 행 스타일 */
    .grid-row {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        width: 100%;
        border-top: 1px solid #3e4452;
        border-bottom: 1px solid #3e4452;
    }
    .grid-cell {
        height: 100px;
        border-left: 1px solid #3e4452;
        border-right: 1px solid #3e4452;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    /* 원형 노드 스타일 */
    .node-circle {
        position: absolute;
        width: 85px;
        height: 85px;
        background: radial-gradient(circle, #2c3e50 0%, #000000 100%);
        border: 3px solid #00d4ff;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 10;
        box-shadow: 0px 0px 15px rgba(0, 212, 255, 0.5);
        transform: translateY(-50%);
    }
    /* 사각형 내 텍스트 스타일 */
    .node-square {
        width: 90%;
        height: 80%;
        background-color: #262a33;
        border: 2px solid #ffeb3b;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .addr { color: #ffffff; font-size: 11px; font-weight: bold; }
    .grain { color: #00d4ff; font-size: 9px; }
    .qty { color: #ffeb3b; font-size: 12px; font-weight: bold; }
    .off { color: #4b5563; font-size: 10px; border-color: #3e4452 !important; background: transparent !important; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 일일 장치장별 & 곡종별 재고현황 (Advanced 5-Row Layout)")

# 2. 데이터 입력
st.sidebar.markdown("### 📋 데이터 입력 (Copy & Paste)")
raw_data = st.sidebar.text_area("주소 곡종 재고량", placeholder="A101 강력분 100.5", height=400)

data_dict = {}
if raw_data.strip():
    try:
        lines = raw_data.strip().split('\n')
        for line in lines:
            parts = line.split()
            if len(parts) >= 3:
                data_dict[parts[0]] = {"grain": parts[1], "qty": float(parts[2])}
        st.sidebar.success(f"✅ {len(data_dict)}개 데이터 매핑됨")
    except:
        st.sidebar.error("형식을 확인해주세요 (주
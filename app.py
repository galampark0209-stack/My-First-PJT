import streamlit as st
import pandas as pd
import io

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고현황 시스템", layout="wide")

# 다크 테마 및 격자선 위 노드 배치 CSS
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .grid-container {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        grid-template-rows: repeat(2, 200px);
        gap: 0px;
        position: relative;
        background-color: #1a1c24;
        border: 1px solid #3e4452;
        margin: 80px auto;
        width: 85%;
    }
    .grid-item { border: 1px solid #2d3139; position: relative; }
    .node {
        position: absolute;
        width: 90px;
        height: 90px;
        background: radial-gradient(circle, #2c3e50 0%, #000000 100%);
        border: 3px solid #00d4ff;
        border-radius: 50%;
        color: #ffffff;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        z-index: 20;
        transform: translate(-50%, -50%);
        box-shadow: 0px 0px 12px rgba(0, 212, 255, 0.6);
    }
    .node-off { border: 2px dashed #3e4452; background: #1a1c24; color: #4b5563; box-shadow: none; }
    .qty { color: #ffeb3b; font-weight: bold; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

st.title("📊 일일 장치장별 & 곡종별 재고현황")

# 2. 데이터 입력 및 콤마 처리
st.sidebar.markdown("### 📋 데이터 입력")
raw_data = st.sidebar.text_area("주소 곡종 재고량", placeholder="A101 강력분 1,500.0", height=400)

data_dict = {}
if raw_data.strip():
    try:
        for line in raw_data.strip().split('\n'):
            parts = line.split()
            if len(parts) >= 3:
                addr = parts[0]
                grain = parts[1]
                # 콤마 제거 로직 유지
                qty_val = float(parts[2].replace(',', ''))
                data_dict[addr] = {"grain": grain, "qty": qty_val}
        st.sidebar.success("데이터 로드 완료")
    except:
        st.sidebar.error("데이터 형식 오류 (콤마/공백 확인)")

# 3. 주소 리스트 (A101~A506 매핑을 위한 3행 18개 구조)
# 람님의 편의를 위해 A1~A3 계열을 우선 매핑합니다.
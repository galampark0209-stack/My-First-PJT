import streamlit as st
import pandas as pd
import io

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고현황 시스템", layout="wide")

# 다크 테마 및 격자/노드 CSS
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
        width: 85px;
        height: 85px;
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

# 2. 데이터 입력
st.sidebar.markdown("### 📋 데이터 입력")
raw_data = st.sidebar.text_area("주소 곡종 재고량", placeholder="A101 강력분 150.0", height=400)

data_dict = {}
if raw_data.strip():
    try:
        for line in raw_data.strip().split('\n'):
            parts = line.split()
            if len(parts) >= 3:
                data_dict[parts[0]] = {"grain": parts[1], "qty": float(parts[2])}
        st.sidebar.success("데이터 로드 완료")
    except:
        st.sidebar.error("형식 오류")

# 3. 주소 리스트 정의 (3행 x 6열 = 18개)
address_map = [
    ["A101", "A102", "A103", "A104", "A105", "A106"], # 상단 라인
    ["A201", "A202", "A203", "A204", "A205", "A206"], # 중간 라인 (원래 7개였으나 6개 접점으로 통일)
    ["A301", "A302", "A303", "A304", "A305", "A306"]  # 하단 라인 (A501 등은 람님의 필요에 따라 수정 가능)
]
# 만약 A501까지 5개 층이 필요하다면 y_positions를 늘리면 됩니다. 
# 일단 텍스트 아트의 2행 격자 구조(3개 가로선)에 맞췄습니다.

y_positions = [0, 50, 100] # 상, 중, 하 가로선 위치
x_positions = [14.28, 28.57, 42.85, 57.14, 71.42, 85.71] # 세로선 교차점

grid_html = '<div class="grid-container">'
for _ in range(14): # 7x2 배경 격자
    grid_html += '<div class="grid-item"></div>'

for r_idx, y_pos in enumerate(y_positions):
    for c_idx, x_pos in enumerate(x_positions):
        addr = address_map[r_idx][c_idx]
        info = data_dict.get(addr)
        
        if info:
            grid_html += f"""
            <div class="node" style="left:{x_pos}%; top:{y_pos}%;">
                <span style="font-weight:bold;">{addr}</span>
                <span style="font-size:9px;">{info['grain']}</span>
                <div style="border-top:1px solid #00d4ff; width:60%; margin:2px 0;"></div>
                <span class="qty">{info['qty']:,.1f}</span>
            </div>"""
        else:
            grid_html += f'<div class="node node-off" style="left:{x_pos}%; top:{y_pos}%;">{addr}</div>'

grid_html += '</div>'
st.markdown(grid_html, unsafe_allow_html=True)
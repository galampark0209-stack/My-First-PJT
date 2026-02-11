import streamlit as st
import pandas as pd

# 1. 페이지 설정 및 제목 변경
st.set_page_config(page_title="일일 재고현황 시스템", layout="wide")

# CSS 스타일 (그리드 및 원형 노드 디자인 고정)
st.markdown("""
<style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        grid-template-rows: repeat(2, 180px);
        gap: 0px;
        position: relative;
        background-color: #ffffff;
        border: 2px solid #2c3e50;
        margin: 60px auto;
        width: 85%;
    }
    .grid-item {
        border: 0.5px solid #eee;
        position: relative;
    }
    .node {
        position: absolute;
        width: 110px;
        height: 110px;
        background-color: #34495e;
        border: 3px solid #3498db;
        border-radius: 50%;
        color: white;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        text-align: center;
        z-index: 10;
        transform: translate(-50%, -50%);
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
    }
    .node-placeholder {
        background-color: #f8f9fa;
        color: #bdc3c7;
        border: 2px dashed #dcdde1;
        box-shadow: none;
    }
</style>
""", unsafe_allow_html=True)

# 요구하신 제목으로 변경
st.title("📊 일일 장치장별&곡종별 재고현황")

# 사이드바 진행도
st.sidebar.write("### 🏁 개발 진행도: 100%")
st.sidebar.progress(100)

uploaded_file = st.file_uploader("데이터 업데이트를 위해 엑셀 파일을 선택하세요", type=['xlsx'])

# 7x2 그리드 내 6개의 접점 좌표 (좌측부터의 백분율)
node_positions = [14.28, 28.57, 42.85, 57.14, 71.42, 85.71]

# 그리드 및 노드 렌더링
grid_html += f"""
<div class="node" style="left: {x_pos}%; top: 50%;">
    <b style="font-size:12px;">{row['장치장']}</b>
    <span>{row['곡종']}</span>
    <div style="border-top:1px solid #fff; width:60%; margin:3px 0;"></div>
    <b>{row['재고량']:.1f}</b>
</div>
"""

# 데이터 매핑 로직
df = None
if uploaded_file:
    df = pd.read_excel(uploaded_file)

for i, x_pos in enumerate(node_positions):
    # 데이터가 있고, 해당 인덱스의 행이 존재하는 경우 실데이터 출력
    if df is not None and i < len(df):
        row = df.iloc[i]
        grid_html += f"""
        <div class="node" style="left: {x_pos}%; top: 50%;">
            <b style="font-size:12px;">{row['장치장']}</b>
            <span>{row['곡종']}</span>
            <div style="border-top:1px solid #fff; width:60%; margin:3px 0;"></div>
            <b>{row['재
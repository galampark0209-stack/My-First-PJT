import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고현황 시스템", layout="wide")

# 2. CSS 스타일
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
    .grid-item { border: 0.5px solid #eee; position: relative; }
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
    .node-placeholder { background-color: #f8f9fa; color: #bdc3c7; border: 2px dashed #dcdde1; }
</style>
""", unsafe_allow_html=True)

st.title("📊 일일 장치장별&곡종별 재고현황")

st.sidebar.write("### 🏁 개발 진행도: 100%")
st.sidebar.progress(100)

uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=['xlsx'])

node_positions = [14.28, 28.57, 42.85, 57.14, 71.42, 85.71]

grid_html = '<div class="grid-container">'
for _ in range(14):
    grid_html += '<div class="grid-item"></div>'

df = None
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error: {e}")

# 에러가 났던 핵심 로직 구간
for i, x_pos in enumerate(node_positions):
    # 아래 라인에 반드시 ':'가 포함되어야 합니다.
    if df is not None and i < len(df):
        try:
            v_loc = str(df.iloc[i]['장치장'])
            v_grain = str(df.iloc[i]['곡종'])
            v_qty = float(df.iloc[i]['재고량'])
            
            grid_html += f'<div class="node" style="left: {x_pos}%; top: 50%;">'
            grid_html += f'<b style="font-size:12px;">{v_loc}</b>'
            grid_html += f'<span>{v_grain}</span>'
            grid_html += '<div style="border-top:1px solid #fff; width:60%; margin:3px 0;"></div>'
            grid_html += f'<b>{v_qty:.1f}</b></div>'
        except Exception:
            grid_html += f'<div class="node node-placeholder" style="left: {x_pos}%; top: 50%;">Data Err</div>'
    else:
        grid_html += f'<div class="node node-placeholder" style="left: {x_pos}%; top: 50%;">대기중</div>'

grid_html += '</div>'
st.markdown(grid_html, unsafe_allow_html=True)
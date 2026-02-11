import streamlit as st
import pandas as pd

st.set_page_config(page_title="일일 재고현황 시스템", layout="wide")

# CSS 스타일: 3개 행의 노드를 배치하기 위한 설정
st.markdown("""
<style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        grid-template-rows: repeat(2, 200px);
        gap: 0px;
        position: relative;
        background-color: #ffffff;
        border: 2px solid #2c3e50;
        margin: 80px auto;
        width: 85%;
    }
    .grid-item { border: 0.5px solid #ddd; position: relative; }
    .node {
        position: absolute;
        width: 90px;
        height: 90px;
        background-color: #34495e;
        border: 2px solid #3498db;
        border-radius: 50%;
        color: white;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        text-align: center;
        z-index: 10;
        transform: translate(-50%, -50%);
        box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
    }
    .node-placeholder { background-color: #f8f9fa; color: #bdc3c7; border: 1.5px dashed #dcdde1; }
</style>
""", unsafe_allow_html=True)

st.title("📊 일일 장치장별&곡종별 재고현황 (3-Row Layout)")

uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=['xlsx'])

# 3개 행(상, 중, 하)의 Y축 위치 (%)
y_positions = [0, 50, 100]
# 가로 6개 접점의 X축 위치 (%)
x_positions = [14.28, 28.57, 42.85, 57.14, 71.42, 85.71]

grid_html = '<div class="grid-container">'
for _ in range(14):
    grid_html += '<div class="grid-item"></div>'

df = None
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error: {e}")

# 3개 행 x 6개 열 = 총 18개 노드 생성 로직
node_count = 0
for y_idx, y_pos in enumerate(y_positions):
    for x_idx, x_pos in enumerate(x_positions):
        # 데이터 매핑 (18개까지 지원)
        if df is not None and node_count < len(df):
            try:
                v_loc = str(df.iloc[node_count]['장치장'])
                v_grain = str(df.iloc[node_count]['곡종'])
                v_qty = float(df.iloc[node_count]['재고량'])
                
                grid_html += f'<div class="node" style="left: {x_pos}%; top: {y_pos}%;">'
                grid_html += f'<b>{v_loc}</b><br><span>{v_grain}</span>'
                grid_html += f'<div style="border-top:1px solid #fff; width:60%; margin:2px 0;"></div>'
                grid_html += f'<b>{v_qty:.1f}</b></div>'
            except:
                grid_html += f'<div class="node node-placeholder" style="left: {x_pos}%; top: {y_pos}%;">Err</div>'
        else:
            grid_html += f'<div class="node node-placeholder" style="left: {x_pos}%; top: {y_pos}%;">대기중</div>'
        
        node_count += 1

grid_html += '</div>'
st.markdown(grid_html, unsafe_allow_html=True)
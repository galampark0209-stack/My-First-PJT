import streamlit as st
import pandas as pd
import io

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고현황 시스템", layout="wide")

# CSS 스타일 (3개 행 노드 배치)
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

st.title("📊 일일 장치장별&곡종별 재고현황")

# 2. 데이터 입력 섹션 (보안을 고려한 Text Area 방식)
st.sidebar.header("📋 데이터 입력")
raw_data = st.sidebar.text_area(
    "엑셀 데이터를 복사해서 아래에 붙여넣으세요:",
    placeholder="예시:\n장치장1  밀가루  150.5\n장치장2  호밀    80.0",
    height=300
)

# 3. 데이터 파싱 로직
df = None
if raw_data.strip():
    try:
        # 공백이나 탭으로 구분된 텍스트를 데이터프레임으로 읽어옴
        df = pd.read_csv(io.StringIO(raw_data), sep=r'\s+', names=['장치장', '곡종', '재고량'])
        st.sidebar.success(f"{len(df)}개의 데이터가 로드되었습니다.")
    except Exception as e:
        st.sidebar.error(f"데이터 형식 오류: {e}")

# 4. 레이아웃 렌더링
y_positions = [0, 50, 100] # 상, 중, 하 3행
x_positions = [14.28, 28.57, 42.85, 57.14, 71.42, 85.71] # 가로 6개 접점

grid_html = '<div class="grid-container">'
for _ in range(14):
    grid_html += '<div class="grid-item"></div>'

node_count = 0
for y_pos in y_positions:
    for x_pos in x_positions:
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
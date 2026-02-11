import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="제분 공정 레이아웃", layout="wide")

# CSS를 이용한 7x2 그리드 및 원형 노드 디자인
st.markdown("""
<style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        grid-template-rows: repeat(2, 150px);
        gap: 0px;
        position: relative;
        background-color: #f0f2f6;
        border: 2px solid #333;
        margin: 50px auto;
        width: 90%;
    }
    .grid-item {
        border: 1px solid #ccc;
        position: relative;
    }
    .node {
        position: absolute;
        width: 100px;
        height: 100px;
        background-color: #1f77b4;
        border-radius: 50%;
        color: white;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        text-align: center;
        z-index: 10;
        transform: translate(-50%, -50%); /* 중심 정렬 */
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    }
    .node b { font-size: 12px; }
</style>
""", unsafe_allow_html=True)

st.title("🏗️ 장치장별 재고 현황 레이아웃 (7x2 Grid)")

uploaded_file = st.file_uploader("재고현황 엑셀 파일을 업로드하세요", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # 그리드 시작 (HTML 생성)
    grid_html = '<div class="grid-container">'
    
    # 14개의 셀 생성
    for i in range(14):
        grid_html += '<div class="grid-item"></div>'
    
    # 모서리가 만나는 지점에 노드 배치 (상단 1줄과 하단 1줄 사이 접점 6개 예시)
    # 실제 데이터의 개수에 따라 루프를 돌며 배치합니다.
    for index, row in df.iterrows():
        if index < 6:  # 가로 7개 사이의 접점은 6개입니다.
            left_pos = (index + 1) * (100 / 7)
            grid_html += f"""
            <div class="node" style="left: {left_pos}%; top: 50%;">
                <b>{row['장치장']}</b>
                <span>{row['곡종']}</span>
                <hr style="width:80%; margin:2px;">
                <span>{row['재고량']:.1f}t</span>
            </div>
            """
    
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)
    st.success("레이아웃 렌더링 완료")
else:
    st.info("파일을 업로드하면 7x2 그리드 레이아웃에 데이터가 표시됩니다.")
import streamlit as st
import pandas as pd
import io

# 1. 페이지 설정 및 다크 테마 적용
st.set_page_config(page_title="실시간 재고현황 시스템", layout="wide")

# 고사양 UI를 위한 CSS 커스텀
st.markdown("""
<style>
    /* 전체 배경 및 폰트 설정 */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* 7x2 그리드 컨테이너 */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        grid-template-rows: repeat(2, 220px);
        gap: 0px;
        position: relative;
        background-color: #1a1c24;
        border: 2px solid #3e4452;
        margin: 100px auto;
        width: 90%;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.5);
    }
    
    /* 그리드 내부 칸 */
    .grid-item {
        border: 1px solid #2d3139;
        position: relative;
    }

    /* 원형 노드 (Status Node) */
    .node {
        position: absolute;
        width: 95px;
        height: 95px;
        background: radial-gradient(circle, #2c3e50 0%, #000000 100%);
        border: 3px solid #00d4ff; /* 네온 블루 테두리 */
        border-radius: 50%;
        color: #00d4ff;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        text-align: center;
        z-index: 10;
        transform: translate(-50%, -50%);
        box-shadow: 0px 0px 15px rgba(0, 212, 255, 0.6);
        font-weight: bold;
    }
    
    /* 데이터가 없을 때의 노드 */
    .node-placeholder {
        background: #1a1c24;
        color: #4b5563;
        border: 2px dashed #3e4452;
        box-shadow: none;
    }

    /* 텍스트 스타일링 */
    .node b { color: #ffffff; font-size: 13px; }
    .node .qty { color: #ffeb3b; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 일일 장치장별 & 곡종별 재고현황 시스템")

# 2. 사이드바 데이터 입력 (보안 방식)
st.sidebar.markdown("### 🛠️ DATA CONTROL")
raw_data = st.sidebar.text_area(
    "데이터를 붙여넣으세요 (장치장 곡종 재고량)",
    placeholder="예시:\nSilo-01  강력분  450.5\nSilo-02  중력분  230.0",
    height=400
)

# 데이터 파싱
df = None
if raw_data.strip():
    try:
        df = pd.read_csv(io.StringIO(raw_data), sep=r'\s+', names=['장치장', '곡종', '재고량'])
        st.sidebar.success(f"✅ {len(df)} Nodes Active")
    except Exception as e:
        st.sidebar.error("데이터 형식을 확인해주세요.")

# 3. 레이아웃 렌더링 (3개 행 x 6개 접점)
y
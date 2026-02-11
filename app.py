import streamlit as st
import pandas as pd
import io

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고현황 시스템", layout="wide")

# CSS: 다크 테마 및 고사양 산업용 UI
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-container {
        position: relative;
        width: 90%;
        margin: 80px auto;
        display: flex;
        flex-direction: column;
    }
    /* 배경 격자 */
    .grid-bg {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        grid-template-rows: repeat(2, 220px);
        width: 100%;
        border: 1px solid #3e4452;
        background-color: #1a1c24;
        position: relative;
    }
    .grid-item { border: 1px solid #2d3139; display: flex; align-items: center; justify-content: center; }
    
    /* 노드 공통 */
    .node-base { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 10; }
    
    /* 원형 노드 (라인 위 배치) */
    .circle {
        position: absolute; width: 90px; height: 90px;
        background: radial-gradient(circle, #2c3e50 0%, #000000 100%);
        border: 3px solid #00d4ff; border-radius: 50%;
        transform: translate(-50%, -50%);
        box-shadow: 0px 0px 15px rgba(0, 212, 255, 0.6);
    }
    
    /* 사각형 노드 (격자 내부 배치) */
    .square {
        width: 90%; height: 85%;
        background-color: #262a33; border: 2px solid #ffeb3b;
    }
    
    /* 텍스트 스타일 */
    .addr { font-size: 11px; font-weight: bold; color: #ffffff; }
    .grain { font-size: 9px; color: #00d4ff; }
    .qty { font-size: 12px; font-weight: bold; color: #ffeb3b; }
    .off { border: 1.5px dashed #444 !important; background: transparent !important; box-shadow: none !important; color: #444 !important; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 일일 장치장별 & 곡종별 재고현황")

# 2. 데이터 처리
st.sidebar.markdown("### 📋 데이터 입력")
raw_data = st.sidebar.text_area("주소 곡종 재고량", height=350)
data_dict = {}
if raw_data.strip():
    for line in raw_data.strip().split('\n'):
        p = line.split()
        if len(p) >= 3:
            try:
                data_dict[p[0]] = {"g": p[1], "q": float(p[2].replace(',', ''))}
            except: continue

# 3. 렌더링 헬퍼 함수
def draw_node(addr, is_circle=True, x=0, y=0):
    val = data_dict.get(addr)
    cls = "circle" if is_circle else "square"
    pos = f"left:{x}%; top:{y}%;" if is_circle else ""
    
    if val:
        return f"""<div class="node-base {cls}" style="{pos}">
            <span class="addr">{addr}</span><span class="grain">{val['g']}</span>
            <div style="border-top:1px solid #555; width:60%; margin:3px 0;"></div>
            <span class="qty">{val['q']:,.1f}</span></div>"""
    return f'<div class="node-base {cls} off" style="{pos}"><span class="addr">{addr}</span></div>'

# 4. 레이아웃 구축
x_pts = [14.28, 28.57, 42.85, 57.14, 71.42, 85.71]
html = '<div class="main-container"><div class="grid-bg">'

# [배경 사각형 14개]
for _ in range(14): html += '<div class="grid-item"></div>'

# [1행: A101-106 원형 - 상단선]
for i, x in enumerate(x_pts): html += draw_node(f"A10{i+1}", True, x, 0)

# [2행: A201-207 사각형 - 1층 내부]
# 사각형은 grid-item 내부로 직접 삽입하기 위해 로직을 분리하지 않고 배경 루프와 맞출 수도 있으나, 
# 안정성을 위해 절대 좌표가 아닌 그리드 시스템을 활용합니다. (아래 5번 섹션에서 통합)

html += '</div></div>' # 임시 닫기

# --- 다시 그리기 (안전한 통합 버전) ---
full_html = '<div class="main-container"><div class="grid-bg">'
# 배경 및 사각형 노드(2, 4행) 배치
for row_idx in [2, 4]:
    for col_idx in range(1, 8):
        addr = f"A{row_idx}0{col_idx}"
        full_html += f'<div class="grid-item">{draw_node(addr, False)}</div>'

# 원형 노드(1, 3, 5행) 덮어씌우기
y_map = {1: 0, 3: 50, 5: 100}
for r, y in y_map.items():
    for i, x in enumerate(x_pts):
        full_html += draw_node(f"A{r}0{i+1}", True, x, y)

full_html += '</div></div>'
st.markdown(full_html, unsafe_allow_html=True)
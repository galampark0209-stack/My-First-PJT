import streamlit as st
import pandas as pd
import io

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고현황 시스템", layout="wide")

# CSS 커스텀 (5개 행 레이아웃)
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
        gap: 80px;
    }
    .row {
        position: relative;
        width: 100%;
        height: 100px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
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

st.title("🚀 일일 장치장별 & 곡종별 재고현황 시스템")

# 2. 데이터 입력 섹션
st.sidebar.markdown("### 📋 DATA INPUT")
raw_data = st.sidebar.text_area("주소 곡종 재고량", placeholder="A101 강력분 100.5", height=400)

data_dict = {}
if raw_data.strip():
    try:
        lines = raw_data.strip().split('\n')
        for line in lines:
            parts = line.split()
            if len(parts) >= 3:
                data_dict[parts[0]] = {"grain": parts[1], "qty": float(parts[2])}
        # 에러가 났던 지점: 문장을 단순화하여 한 줄에 배치함
        st.sidebar.success("Success")
    except:
        st.sidebar.error("Error")

# 3. 노드 렌더링 함수
def render_node(addr, is_circle=True):
    content = data_dict.get(addr)
    style_class = "node-circle" if is_circle else "node-square"
    if content:
        return f'<div class="{style_class}"><span class="addr">{addr}</span><span class="grain">{content["grain"]}</span><div style="border-top:1px solid #555; width:60%; margin:2px 0;"></div><span class="qty">{content["qty"]:,.1f}</span></div>'
    return f'<div class="{style_class} off"><span class="addr">{addr}</span><span style="font-size:8px;">OFFLINE</span></div>'

# 4. 레이아웃 생성
html = '<div class="main-container">'

# 1행 (A101-106 원형)
html += '<div class="row">'
for i in range(1, 7):
    x_pos = i * (100 / 7)
    html += f'<div style="position:absolute; left:{x_pos}%; top:50%;">{render_node(f"A10{i}")}</div>'
html += '</div>'

# 2행 (A201-207 사각형)
html += '<div class="row grid-row">'
for i in range(1, 8):
    html += f'<div class="grid-cell">{render_node(f"A20{i}", False)}</div>'
html += '</div>'

# 3행 (A301-306 원형)
html += '<div class="row">'
for i in range(1, 7):
    x_pos = i * (100 / 7)
    html += f'<div style="position:absolute; left:{x_pos}%; top:50%;">{render_node(f"A30{i}")}</div>'
html += '</div>'

# 4행 (A401-407 사각형)
html += '<div class="row grid-row">'
for i in range(1, 8):
    html += f'<div class="grid-cell">{render_node(f"A40{i}", False)}</div>'
html += '</div>'

# 5행 (A501-506 원형)
html += '<div class="row">'
for i in range(1, 7):
    x_pos = i * (100 / 7)
    html += f'<div style="position:absolute; left:{x_pos}%; top:50%;">{render_node(f"A50{i}")}</div>'
html += '</div>'

html += '</div>'
st.markdown(html, unsafe_allow_html=True)
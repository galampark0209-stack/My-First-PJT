import streamlit as st
import pandas as pd
import io

# 1. 페이지 설정
st.set_page_config(page_title="일일 재고현황 시스템", layout="wide")

# UI 스타일링 (다크 테마)
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-container {
        position: relative; width: 95%; margin: 50px auto;
        background-color: #1a1c24; border: 2px solid #3e4452;
        padding: 40px 0; display: flex; flex-direction: column; gap: 60px;
    }
    .row { position: relative; width: 100%; height: 80px; display: flex; justify-content: center; align-items: center; }
    .grid-row { display: grid; grid-template-columns: repeat(7, 1fr); width: 100%; border-top: 1px solid #333; border-bottom: 1px solid #333; }
    .grid-cell { height: 100px; border-right: 1px solid #333; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    .node-circle {
        position: absolute; width: 80px; height: 80px;
        background: radial-gradient(circle, #2c3e50 0%, #000000 100%);
        border: 2px solid #00d4ff; border-radius: 50%;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        z-index: 10; box-shadow: 0px 0px 10px rgba(0, 212, 255, 0.4); transform: translateY(-50%);
    }
    .node-square { width: 90%; height: 85%; background-color: #262a33; border: 1px solid #ffeb3b; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    .addr { color: #ffffff; font-size: 10px; font-weight: bold; }
    .grain { color: #00d4ff; font-size: 9px; }
    .qty { color: #ffeb3b; font-size: 11px; }
    .off { opacity: 0.3; border-color: #444 !important; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 일일 장치장별 & 곡종별 재고현황")

# 2. 데이터 입력 및 클렌징
st.sidebar.markdown("### 📋 데이터 입력")
raw_data = st.sidebar.text_area("데이터를 붙여넣으세요", height=300)

data_dict = {}
if raw_data.strip():
    try:
        lines = raw_data.strip().split('\n')
        for line in lines:
            parts = line.split()
            if len(parts) >= 3:
                addr = parts[0]
                grain = parts[1]
                # 콤마(,) 제거 후 숫자로 변환
                qty_str = parts[2].replace(',', '')
                data_dict[addr] = {"grain": grain, "qty": float(qty_str)}
        st.sidebar.success(f"✅ {len(data_dict)}개 데이터 로드됨")
    except Exception as e:
        st.sidebar.error(f"오류 발생: {e}")

# 3. 노드 렌더링 함수
def render_node(addr, is_circle=True):
    content = data_dict.get(addr)
    cls = "node-circle" if is_circle else "node-square"
    if content:
        return f'<div class="{cls}"><span class="addr">{addr}</span><span class="grain">{content["grain"]}</span><span class="qty">{content["qty"]:,.1f}</span></div>'
    return f'<div class="{cls} off"><span class="addr">{addr}</span></div>'

# 4. 레이아웃 (A구역 위주 5개 행)
html = '<div class="main-container">'
# 1행: A101~106 (원)
html += '<div class="row">'
for i in range(1, 7):
    x = i * (100/7)
    html += f'<div style="position:absolute; left:{x}%; top:50%;">{render_node(f"A10{i}")}</div>'
html += '</div>'
# 2행: A201~207 (사각형)
html += '<div class="row grid-row">'
for i in range(1, 8):
    html += f'<div class="grid-cell">{render_node(f"A20{i}", False)}</div>'
html += '</div>'
# 3행: A301~306 (원)
html += '<div class="row">'
for i in range(1, 7):
    x = i * (100/7)
    html += f'<div style="position:absolute; left:{x}%; top:50%;">{render_node(f"A30{i}")}</div>'
html += '</div>'
# 4행: A401~407 (사각형)
html += '<div class="row grid-row">'
for i in range(1, 8):
    html += f'<div class="grid-cell">{render_node(f"A40{i}", False)}</div>'
html += '</div>'
# 5행: A501~506 (원)
html += '<div class="row">'
for i in range(1, 7):
    x = i * (100/7)
    html += f'<div style="position:absolute; left:{x}%; top:50%;">{render_node(f"A50{i}")}</div>'
html += '</div>'
html += '</div>'
st.markdown(html, unsafe_allow_html=True)

# 5. 기타 데이터 (B, T, W 구역) 표 형식 제공
if data_dict:
    with st.expander("📝 기타 구역 데이터 (B, T, W, etc.)"):
        other_data = {k: v for k, v in data_dict.items() if not k.startswith('A')}
        if other_data:
            st.table(pd.DataFrame.from_dict(other_data, orient='index'))
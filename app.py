import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="제분업 재고 관리", layout="wide")

st.sidebar.write("### 🏁 개발 진행도: 90%")
st.sidebar.progress(90)

st.title("🌾 제분 실시간 재고 관리 시스템")

# 파일 업로드 (Constraint 6 충족)
uploaded_file = st.file_uploader("재고현황 엑셀(.xlsx) 파일을 업로드하세요", type=['xlsx'])

if uploaded_file is not None:
    # 주석: 엑셀 데이터를 읽어옵니다. 
    df = pd.read_excel(uploaded_file)
    
    # 주석: 데이터 타입 강제 지정 (데이터 정합성 확보)
    # 재고량 열을 십진수(float) 형태로 변환하여 계산 오류를 방지합니다.
    if '재고량' in df.columns:
        df['재고량'] = df['재고량'].astype(float)
    
    # 화면 출력
    st.success("데이터가 성공적으로 로드되었습니다.")
    
    # 3. 데이터 요약 통계 (추론 답변 근거)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 전체 재고 현황")
        st.dataframe(df, use_container_width=True)
    
    with col2:
        st.subheader("📈 곡종별 총 재고량")
        # 주석: 곡종별로 그룹화하여 재고량의 합계를 구합니다.
        summary = df.groupby('곡종')['재고량'].sum()
        st.bar_chart(summary)

else:
    st.info("💡 [장치장, 곡종, 재고량] 컬럼이 포함된 엑셀 파일을 업로드해 주세요.")
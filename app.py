import streamlit as st

st.set_page_config(
    page_title="Philip Kim Research Lab",
    page_icon="",
    layout="wide"
)

st.title("Philip Kim Research Lab")

st.subheader("AI, Semiconductor, Data Science")

st.write("""
이 홈페이지는 Streamlit으로 만든 연구·강의·데이터 분석용 홈페이지입니다.

왼쪽 메뉴에서 연구 주제, 강의 자료, 데이터 대시보드를 선택할 수 있도록 확장할 예정입니다.
""")

st.divider()

st.header("Research Topics")

st.write("""
1. HBM Transition and Semiconductor Ecosystem
2. DRAM Market Analytics
3. Machine Learning Education
4. AI Strategy and Industrial Transformation
""")

st.header("Contact")

st.write("GitHub Blog, LinkedIn, Email 등을 여기에 연결하면 됩니다.")

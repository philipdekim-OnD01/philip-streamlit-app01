import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Philip Kim Deep Learning Lab",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&display=swap');

    :root {
        --ink: #162033;
        --muted: #5b6475;
        --line: #dfe6f1;
        --blue: #2563eb;
        --cyan: #06b6d4;
        --green: #16a34a;
        --orange: #f97316;
        --panel: #ffffff;
        --soft: #f4f7fb;
    }

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .block-container {
        padding-top: 2.1rem;
        padding-bottom: 4rem;
        max-width: 1220px;
    }

    [data-testid="stSidebar"] {
        background: #f7f9fd;
        border-right: 1px solid var(--line);
    }

    .hero {
        position: relative;
        overflow: hidden;
        border: 1px solid #d9e4f5;
        border-radius: 18px;
        padding: 44px 48px;
        background:
            radial-gradient(circle at 86% 18%, rgba(37, 99, 235, .18), transparent 28%),
            radial-gradient(circle at 90% 78%, rgba(6, 182, 212, .15), transparent 30%),
            linear-gradient(135deg, #f8fbff 0%, #eef5ff 52%, #f7fbff 100%);
        box-shadow: 0 20px 60px rgba(22, 32, 51, .08);
    }

    .hero:after {
        content: "";
        position: absolute;
        right: -80px;
        top: -70px;
        width: 320px;
        height: 320px;
        border: 1px solid rgba(37, 99, 235, .16);
        border-radius: 50%;
    }

    .eyebrow {
        display: inline-flex;
        gap: 8px;
        align-items: center;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(37, 99, 235, .1);
        color: #1d4ed8;
        font-size: 14px;
        font-weight: 800;
        letter-spacing: .02em;
    }

    .hero h1,
    .hero h2 {
        margin: 18px 0 14px;
        color: var(--ink);
        font-size: 54px;
        line-height: 1.08;
        letter-spacing: 0;
        font-weight: 800;
        max-width: 880px;
    }

    .hero p {
        margin: 0;
        max-width: 760px;
        color: var(--muted);
        font-size: 20px;
        line-height: 1.65;
        font-weight: 500;
    }

    .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 28px;
    }

    .pill {
        padding: 10px 14px;
        border-radius: 999px;
        background: #fff;
        border: 1px solid #dce6f4;
        color: #2f3a4c;
        font-weight: 700;
        box-shadow: 0 8px 18px rgba(22, 32, 51, .05);
    }

    .section-title {
        margin: 34px 0 14px;
        color: var(--ink);
        font-size: 30px;
        font-weight: 800;
    }

    .section-subtitle {
        margin: -6px 0 20px;
        color: var(--muted);
        font-size: 17px;
        line-height: 1.6;
    }

    .metric-card,
    .course-card,
    .note-card {
        height: 100%;
        padding: 22px 22px;
        border: 1px solid var(--line);
        border-radius: 14px;
        background: var(--panel);
        box-shadow: 0 12px 34px rgba(22, 32, 51, .06);
        transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }

    .metric-card:hover,
    .course-card:hover,
    .note-card:hover {
        transform: translateY(-3px);
        border-color: #b8cdf5;
        box-shadow: 0 18px 42px rgba(22, 32, 51, .1);
    }

    .metric-card .value {
        color: var(--blue);
        font-size: 34px;
        font-weight: 800;
        line-height: 1;
    }

    .metric-card .label {
        margin-top: 8px;
        color: var(--muted);
        font-size: 15px;
        font-weight: 700;
    }

    .course-card .tag {
        display: inline-block;
        padding: 5px 9px;
        border-radius: 8px;
        background: #edf4ff;
        color: #1d4ed8;
        font-size: 13px;
        font-weight: 800;
    }

    .course-card h3 {
        margin: 14px 0 8px;
        color: var(--ink);
        font-size: 21px;
        font-weight: 800;
    }

    .course-card p,
    .note-card p {
        margin: 0;
        color: var(--muted);
        font-size: 15.5px;
        line-height: 1.55;
    }

    .step {
        display: grid;
        grid-template-columns: 54px 1fr;
        gap: 14px;
        align-items: start;
        margin-bottom: 14px;
        padding: 16px;
        border: 1px solid var(--line);
        border-radius: 12px;
        background: #fff;
    }

    .step .num {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: #162033;
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
    }

    .step h4 {
        margin: 0 0 4px;
        color: var(--ink);
        font-size: 17px;
        font-weight: 800;
    }

    .step p {
        margin: 0;
        color: var(--muted);
        font-size: 14.5px;
        line-height: 1.5;
    }

    .code-box {
        padding: 20px 22px;
        border-radius: 14px;
        background: #101827;
        color: #dce7ff;
        border: 1px solid #263245;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 15px;
        line-height: 1.65;
        white-space: pre-wrap;
    }

    .footer {
        margin-top: 42px;
        padding: 22px;
        border-radius: 14px;
        background: #162033;
        color: #dbe7ff;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.markdown("### Philip Kim Lab")
    st.caption("Deep Learning Lecture Portal")
    st.divider()
    st.markdown("**첫 화면 구성**")
    st.markdown("- 딥러닝 강의 로드맵")
    st.markdown("- 실습 중심 학습 흐름")
    st.markdown("- Vision 이상탐지 예제")
    st.markdown("- 수업 자료 게시 예정")
    st.info("왼쪽 페이지 메뉴에서 딥러닝 강의 로드맵을 열 수 있습니다.")
    st.divider()
    st.markdown("**바로가기**")
    st.link_button("GitHub Repository", "https://github.com/philipdekim-OnD01/philip-streamlit-app01")
    st.link_button("Streamlit App", "https://philip-app-app01-kim.streamlit.app/")


st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">DEEP LEARNING EDUCATION</div>
        <h2>딥러닝을 수식이 아니라 동작으로 이해하는 강의실</h2>
        <p>
            입력 데이터가 모델을 지나 예측값이 되고, 손실 함수와 역전파를 통해 가중치가 바뀌는 과정을
            초급자도 따라올 수 있도록 시각화와 실습 중심으로 정리합니다.
        </p>
        <div class="hero-actions">
            <div class="pill">PyTorch 실습</div>
            <div class="pill">CNN Vision</div>
            <div class="pill">이상탐지</div>
            <div class="pill">반도체·의료 이미지 예제</div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="section-title">오늘 배울 핵심</div>', unsafe_allow_html=True)
metric_cols = st.columns(4)
metrics = [
    ("01", "데이터", "이미지와 라벨을 텐서로 바꾸는 과정"),
    ("02", "모델", "DNN, CNN이 입력을 예측값으로 바꾸는 방식"),
    ("03", "학습", "loss, backward, optimizer의 실제 역할"),
    ("04", "평가", "accuracy, recall, F1, ROC-AUC 해석"),
]

for col, (value, label, desc) in zip(metric_cols, metrics):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="value">{value}</div>
                <div class="label">{label}</div>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


left, right = st.columns([1.05, 0.95], gap="large")

with left:
    st.markdown('<div class="section-title">강의 로드맵</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">처음 보는 학생도 코드 실행 순서대로 이해할 수 있게 구성했습니다.</div>',
        unsafe_allow_html=True,
    )

    roadmap = [
        ("1", "텐서와 데이터셋", "MNIST/FashionMNIST 이미지를 텐서로 읽고, batch가 왜 필요한지 이해합니다."),
        ("2", "DNN 기본 구조", "Flatten, Linear, ReLU, CrossEntropyLoss, Adam optimizer를 연결합니다."),
        ("3", "CNN과 이미지 특징", "Convolution, pooling, channel 개념을 그림과 코드로 연결합니다."),
        ("4", "Vision 이상탐지", "정상 데이터만 학습하고 재구성 오차 또는 확신 부족으로 이상 점수를 만듭니다."),
    ]

    for num, title, body in roadmap:
        st.markdown(
            f"""
            <div class="step">
                <div class="num">{num}</div>
                <div>
                    <h4>{title}</h4>
                    <p>{body}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with right:
    st.markdown('<div class="section-title">학습 루프 한눈에 보기</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">딥러닝 수업에서 가장 중요한 코드는 아래 5단계입니다.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="code-box">for x, y in loader:
    logit = model(x)              # 1. forward
    loss = criterion(logit, y)    # 2. loss
    optimizer.zero_grad()         # 3. grad reset
    loss.backward()               # 4. backprop
    optimizer.step()              # 5. update</div>
        """,
        unsafe_allow_html=True,
    )


st.markdown('<div class="section-title">강의 모듈</div>', unsafe_allow_html=True)
module_cols = st.columns(3)
modules = [
    ("Module 1", "딥러닝 기초", "손실 함수, 옵티마이저, 배치, GPU/MPS 개념을 초급자 언어로 정리합니다."),
    ("Module 2", "CNN Vision 실습", "이미지 픽셀, 채널, 필터, feature map을 실습 코드와 함께 설명합니다."),
    ("Module 3", "이상탐지 프로젝트", "MVTec, Casting, 의료 이미지 예제로 정상/불량 판별 흐름을 만듭니다."),
]

for col, (tag, title, body) in zip(module_cols, modules):
    with col:
        st.markdown(
            f"""
            <div class="course-card">
                <span class="tag">{tag}</span>
                <h3>{title}</h3>
                <p>{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown('<div class="section-title">성능 지표는 이렇게 읽습니다</div>', unsafe_allow_html=True)
chart_cols = st.columns([1.1, 0.9], gap="large")

with chart_cols[0]:
    df = pd.DataFrame(
        {
            "metric": ["Accuracy", "Precision", "Recall", "F1-score", "ROC-AUC"],
            "score": [0.96, 0.84, 0.72, 0.78, 0.91],
        }
    )
    fig = go.Figure(
        data=[
            go.Bar(
                x=df["metric"],
                y=df["score"],
                marker=dict(color=["#2563eb", "#06b6d4", "#16a34a", "#f97316", "#7c3aed"]),
                text=[f"{v:.2f}" for v in df["score"]],
                textposition="outside",
            )
        ]
    )
    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis=dict(range=[0, 1.05], tickformat=".0%"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Noto Sans KR, sans-serif", size=14, color="#162033"),
    )
    st.plotly_chart(fig, use_container_width=True)

with chart_cols[1]:
    st.markdown(
        """
        <div class="note-card">
            <p>
                불량률이 낮은 데이터에서는 accuracy만 보면 위험합니다.
                예를 들어 정상 95%, 불량 5% 데이터에서 전부 정상이라고 예측해도 accuracy는 95%가 됩니다.
                그래서 이상탐지와 의료·공정 데이터에서는 recall, F1-score, PR-AUC를 함께 확인해야 합니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <div class="footer">
        이 페이지는 딥러닝 강의 자료를 올리기 위한 첫 화면입니다.
        다음 단계에서는 각 Module을 개별 페이지로 분리하고, 노트북·Markdown·데이터 실습 링크를 연결하면 됩니다.
    </div>
    """,
    unsafe_allow_html=True,
)

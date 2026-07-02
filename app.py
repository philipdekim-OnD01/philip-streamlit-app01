import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Philip Kim Ondevice AI Education",
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
    st.caption("Ondevice AI Education Portal")
    st.divider()
    st.markdown("**첫 화면 구성**")
    st.markdown("- 머신러닝 기초")
    st.markdown("- 딥러닝 모델 이해")
    st.markdown("- Ondevice AI 응용")
    st.markdown("- 실습·배포 중심 구성")
    st.link_button("Ondevice AI 교육 로드맵", "/Course_Roadmap")
    st.divider()
    st.markdown("**바로가기**")
    st.link_button("GitHub Repository", "https://github.com/philipdekim-OnD01/philip-streamlit-app01")
    st.link_button("Streamlit App", "https://philip-app-app01-kim.streamlit.app/")


st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">ONDEVICE AI EDUCATION</div>
        <h2>머신러닝에서 딥러닝을 지나 Ondevice AI까지</h2>
        <p>
            이 교육은 모델을 외우는 수업이 아니라, 데이터를 이해하고 모델을 학습시킨 뒤
            실제 디바이스 환경에서 작동 가능한 AI 서비스로 연결하는 흐름을 다룹니다.
        </p>
        <div class="hero-actions">
            <div class="pill">Machine Learning</div>
            <div class="pill">Deep Learning</div>
            <div class="pill">Ondevice AI</div>
            <div class="pill">Streamlit 실습</div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.link_button("10주 교육 로드맵 바로 열기", "/Course_Roadmap")


st.markdown('<div class="section-title">교육의 3단계</div>', unsafe_allow_html=True)
metric_cols = st.columns(3)
metrics = [
    ("01", "머신러닝", "데이터, 회귀, 분류, 평가 지표를 통해 AI의 기본 판단 구조를 이해합니다."),
    ("02", "딥러닝", "Tensor, DNN, CNN, loss, backpropagation으로 학습 루프를 해석합니다."),
    ("03", "Ondevice AI", "작은 모델, 빠른 추론, 경량화, 배포를 통해 실제 디바이스 활용으로 연결합니다."),
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
    st.markdown('<div class="section-title">한눈에 보는 로드맵</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">기초 모델 이해에서 디바이스 적용까지 단계적으로 올라갑니다.</div>',
        unsafe_allow_html=True,
    )

    roadmap = [
        ("1", "머신러닝 기초", "OLS, Ridge, Lasso, Naive Bayes, Tree, SVM으로 데이터가 어떻게 예측으로 바뀌는지 봅니다."),
        ("2", "딥러닝 기초", "DNN, CNN, loss, optimizer, batch, GPU/MPS 개념을 코드 중심으로 이해합니다."),
        ("3", "Vision AI 실습", "이미지 분류와 이상탐지를 통해 반도체·의료·제조 데이터 응용 흐름을 만듭니다."),
        ("4", "Ondevice AI 적용", "모델 경량화, 지연시간, 메모리, 배포 관점에서 실제 적용 가능성을 점검합니다."),
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
    st.markdown('<div class="section-title">수업의 핵심 관점</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Ondevice AI는 모델 성능만 보는 수업이 아닙니다.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="code-box">1. 잘 예측하는가?
   accuracy, recall, F1, ROC-AUC

2. 작고 빠르게 만들 수 있는가?
   model size, latency, memory

3. 실제 환경에서 쓸 수 있는가?
   device, sensor, privacy, deployment</div>
        """,
        unsafe_allow_html=True,
    )


st.markdown('<div class="section-title">챕터 소개</div>', unsafe_allow_html=True)
module_cols = st.columns(3)
modules = [
    ("Chapter 1", "머신러닝", "회귀, 분류, 평가 지표, 교차검증을 통해 AI 모델 선택의 기준을 잡습니다."),
    ("Chapter 2", "딥러닝", "DNN/CNN과 학습 루프를 이해하고 이미지 데이터를 다루는 실습으로 확장합니다."),
    ("Chapter 3", "Ondevice AI", "모델을 작고 빠르게 만들어 현장 장치와 서비스에 올리는 관점을 배웁니다."),
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


st.markdown('<div class="section-title">기존 블로그 강의자료 연결</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">obsidian-blog에 정리된 강의자료를 이 Streamlit 앱의 학습 흐름에 맞춰 연결합니다.</div>',
    unsafe_allow_html=True,
)

link_cols = st.columns(4)
blog_links = [
    (
        "AI 수학 기초",
        "행렬, 미분, 경사하강법, softmax, cross entropy",
        "https://philipdekim-ond01.github.io/obsidian-blog/ai-math/",
    ),
    (
        "전체 복습 노트",
        "선형대수부터 머신러닝, 딥러닝, 온디바이스 경량화까지",
        "https://philipdekim-ond01.github.io/obsidian-blog/ai-semiconductor-course-review-ondevice-lightweighting.html",
    ),
    (
        "Ondevice AI 전체지도",
        "라즈베리파이, TFLite, RPS 실습, 전이학습, 경량화",
        "https://philipdekim-ond01.github.io/obsidian-blog/ondevice-ai-00-overview.html",
    ),
    (
        "QAT 실습",
        "DenseNet/ResNet, 데이터 보강, QAT, TFLite 변환",
        "https://philipdekim-ond01.github.io/obsidian-blog/ondevice-ai-04-lightweighting-qat-beginner.html",
    ),
]

for col, (title, desc, url) in zip(link_cols, blog_links):
    with col:
        st.markdown(
            f"""
            <div class="course-card">
                <span class="tag">Blog</span>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.link_button("자료 열기", url, use_container_width=True)


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
                Ondevice AI 교육에서도 성능 지표는 출발점입니다.
                실제 적용에서는 accuracy뿐 아니라 recall, F1-score, latency, memory, 전력 소모까지 함께 봐야 합니다.
                특히 의료·제조·반도체 데이터에서는 놓치면 안 되는 class를 기준으로 평가해야 합니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <div class="footer">
        이 페이지는 Ondevice AI 교육의 첫 화면입니다.
        머신러닝, 딥러닝, Ondevice AI 챕터를 단계적으로 확장하고 수업 자료와 실습 링크를 연결합니다.
    </div>
    """,
    unsafe_allow_html=True,
)

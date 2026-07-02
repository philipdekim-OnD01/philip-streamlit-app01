import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Ondevice AI 교육 로드맵",
    page_icon=None,
    layout="wide",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 1220px;
    }

    .hero {
        padding: 42px 46px;
        border-radius: 18px;
        border: 1px solid #dbe6f7;
        background:
            radial-gradient(circle at 84% 20%, rgba(37, 99, 235, .18), transparent 28%),
            linear-gradient(135deg, #f8fbff 0%, #eef5ff 58%, #ffffff 100%);
        box-shadow: 0 18px 54px rgba(22, 32, 51, .08);
    }

    .hero .label {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        background: #eaf2ff;
        color: #1d4ed8;
        font-size: 14px;
        font-weight: 800;
    }

    .hero h1 {
        margin: 18px 0 12px;
        color: #162033;
        font-size: 50px;
        line-height: 1.12;
        font-weight: 800;
        letter-spacing: 0;
    }

    .hero p {
        margin: 0;
        max-width: 880px;
        color: #5b6475;
        font-size: 19px;
        line-height: 1.65;
        font-weight: 500;
    }

    .section-title {
        margin: 34px 0 14px;
        color: #162033;
        font-size: 30px;
        font-weight: 800;
    }

    .section-subtitle {
        margin: -6px 0 20px;
        color: #5b6475;
        font-size: 16.5px;
        line-height: 1.6;
    }

    .stage-card,
    .topic-card,
    .resource-card {
        height: 100%;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #dfe6f1;
        background: #ffffff;
        box-shadow: 0 12px 34px rgba(22, 32, 51, .06);
    }

    .stage-card {
        border-left: 6px solid #2563eb;
    }

    .stage-card .stage {
        color: #2563eb;
        font-size: 14px;
        font-weight: 800;
    }

    .stage-card h3,
    .topic-card h3,
    .resource-card h3 {
        margin: 8px 0 8px;
        color: #162033;
        font-size: 21px;
        font-weight: 800;
    }

    .stage-card p,
    .topic-card p,
    .resource-card p {
        margin: 0;
        color: #5b6475;
        font-size: 15.5px;
        line-height: 1.58;
    }

    .tag-row {
        margin-top: 14px;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }

    .tag {
        padding: 5px 9px;
        border-radius: 8px;
        background: #f0f6ff;
        color: #1d4ed8;
        font-size: 12.5px;
        font-weight: 800;
    }

    .timeline {
        position: relative;
        padding-left: 22px;
        border-left: 3px solid #dbe6f7;
    }

    .timeline-item {
        position: relative;
        margin-bottom: 18px;
        padding: 18px 20px;
        border-radius: 14px;
        border: 1px solid #dfe6f1;
        background: #fff;
        box-shadow: 0 8px 22px rgba(22, 32, 51, .05);
    }

    .timeline-item:before {
        content: "";
        position: absolute;
        left: -31px;
        top: 23px;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #2563eb;
        border: 4px solid #eaf2ff;
    }

    .timeline-item h4 {
        margin: 0 0 6px;
        color: #162033;
        font-size: 18px;
        font-weight: 800;
    }

    .timeline-item p {
        margin: 0;
        color: #5b6475;
        font-size: 15px;
        line-height: 1.55;
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

    .callout {
        padding: 20px 22px;
        border-radius: 14px;
        background: #162033;
        color: #eaf2ff;
        font-size: 16px;
        line-height: 1.65;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <section class="hero">
        <div class="label">ONDEVICE AI COURSE ROADMAP</div>
        <h1>Ondevice AI 교육 로드맵</h1>
        <p>
            이 과정은 머신러닝으로 예측 문제를 이해하고, 딥러닝으로 이미지와 복잡한 패턴을 학습한 뒤,
            최종적으로 작은 장치에서 동작 가능한 AI로 연결하는 3단계 교육입니다.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="section-title">3단계 챕터 구성</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">참고 폴더의 머신러닝 자료를 출발점으로 두고, 딥러닝과 Ondevice AI로 확장합니다.</div>',
    unsafe_allow_html=True,
)

stage_cols = st.columns(3)
stages = [
    (
        "Chapter 1",
        "머신러닝",
        "데이터를 표 형태로 보고, 어떤 모델이 어떤 방식으로 예측하는지 이해합니다. 회귀, 분류, 평가 지표가 핵심입니다.",
        ["OLS", "Ridge/Lasso", "Tree/SVM", "Model Evaluation"],
    ),
    (
        "Chapter 2",
        "딥러닝",
        "Tensor, DNN, CNN, loss, optimizer, backpropagation을 통해 모델이 스스로 가중치를 바꾸는 과정을 배웁니다.",
        ["Tensor", "DNN", "CNN", "Backprop"],
    ),
    (
        "Chapter 3",
        "Ondevice AI",
        "성능 좋은 모델을 작고 빠르게 만들어 실제 디바이스에서 동작시키는 관점으로 확장합니다.",
        ["Latency", "Memory", "Quantization", "Deployment"],
    ),
]

for col, (stage, title, body, tags) in zip(stage_cols, stages):
    with col:
        tag_html = "".join(f'<span class="tag">{tag}</span>' for tag in tags)
        st.markdown(
            f"""
            <div class="stage-card">
                <div class="stage">{stage}</div>
                <h3>{title}</h3>
                <p>{body}</p>
                <div class="tag-row">{tag_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


left, right = st.columns([1.05, 0.95], gap="large")

with left:
    st.markdown('<div class="section-title">강의 진행 순서</div>', unsafe_allow_html=True)
    timeline = [
        ("01", "AI와 데이터 문제 정의", "예측 대상 y와 입력 X를 나누고, 모델이 무엇을 학습하는지 정리합니다."),
        ("02", "머신러닝 기초 수학", "`y - Xw`, 손실함수, OLS, 미분, 경사하강법의 의미를 연결합니다."),
        ("03", "회귀와 정규화", "Linear Regression, Ridge, Lasso, SVR을 비교하고 과적합을 설명합니다."),
        ("04", "분류 모델", "Naive Bayes, Decision Tree, SVM을 통해 데이터를 나누는 여러 방식을 배웁니다."),
        ("05", "평가 지표", "accuracy, recall, precision, F1, ROC-AUC를 문제 목적에 맞게 해석합니다."),
        ("06", "딥러닝 입문", "Tensor, batch, model, criterion, optimizer가 학습 코드에서 어떤 역할을 하는지 봅니다."),
        ("07", "DNN/CNN Vision", "이미지 데이터를 DNN과 CNN으로 처리하고 feature map 개념을 이해합니다."),
        ("08", "이상탐지 응용", "제조·의료·반도체 이미지에서 정상/불량 판별 흐름을 실습합니다."),
        ("09", "Ondevice AI 입문", "디바이스 제약, 지연시간, 메모리, 전력, 개인정보 보호 관점을 정리합니다."),
        ("10", "모델 경량화와 배포", "모델 크기 축소, quantization, edge deployment의 기본 개념을 다룹니다."),
        ("11", "프로젝트", "작은 AI 모델을 만들고 성능과 디바이스 적용 가능성을 함께 평가합니다."),
        ("12", "Streamlit 발표", "결과를 웹 앱으로 정리해 교육 자료와 데모 형태로 공유합니다."),
    ]

    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for num, title, body in timeline:
        st.markdown(
            f"""
            <div class="timeline-item">
                <h4>{num}. {title}</h4>
                <p>{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-title">수업의 핵심 질문</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="code-box">Chapter 1. 머신러닝
- 어떤 feature가 y를 설명하는가?
- 어떤 모델이 기준선이 되는가?
- 어떤 지표로 평가해야 하는가?

Chapter 2. 딥러닝
- 모델은 어떻게 스스로 학습하는가?
- loss와 backprop은 무엇을 바꾸는가?
- 이미지는 어떻게 feature가 되는가?

Chapter 3. Ondevice AI
- 이 모델을 장치에서 돌릴 수 있는가?
- 빠르고 작게 만들 수 있는가?
- 현장에서 쓸 만큼 안정적인가?</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">수업 설계 원칙</div>', unsafe_allow_html=True)
    principles = [
        ("쉬운 모델에서 시작", "OLS, Tree, SVM으로 예측과 분류의 기본 구조를 먼저 잡습니다."),
        ("딥러닝은 학습 루프로 설명", "모델 구조보다 forward, loss, backward, update 흐름을 먼저 이해합니다."),
        ("Ondevice AI는 제약 조건까지 포함", "정확도뿐 아니라 속도, 메모리, 전력, 배포 가능성을 같이 봅니다."),
    ]
    for title, body in principles:
        st.markdown(
            f"""
            <div class="topic-card" style="margin-bottom: 14px;">
                <h3>{title}</h3>
                <p>{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown('<div class="section-title">참고 자료 매핑</div>', unsafe_allow_html=True)
resource_cols = st.columns(3)
resources = [
    (
        "머신러닝 자료",
        "`y - Xw`, OLS, Ridge, Lasso, Bayes, Tree, SVM",
        "모델이 데이터를 어떻게 예측값으로 바꾸는지 이해하는 기초 자료입니다.",
    ),
    (
        "딥러닝 실습",
        "DNN, CNN, 학습 루프, 이미지 분류, 이상탐지",
        "복잡한 이미지와 비선형 패턴을 다루기 위한 중간 단계입니다.",
    ),
    (
        "Ondevice AI 확장",
        "경량화, 지연시간, 메모리, Streamlit 데모",
        "모델을 실제 사용 가능한 AI 서비스로 바꾸는 마지막 단계입니다.",
    ),
]

for col, (title, source, body) in zip(resource_cols, resources):
    with col:
        st.markdown(
            f"""
            <div class="resource-card">
                <h3>{title}</h3>
                <p><b>{source}</b></p>
                <p style="margin-top: 8px;">{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown('<div class="section-title">obsidian-blog 자료 링크</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">이 로드맵은 아래 블로그 강의자료를 기준으로 Streamlit에서 다시 묶은 것입니다.</div>',
    unsafe_allow_html=True,
)

blog_rows = [
    {
        "단계": "머신러닝 준비",
        "자료": "AI 수학 기초 강의",
        "핵심": "행렬, 미분, 경사하강법, cross entropy",
        "링크": "https://philipdekim-ond01.github.io/obsidian-blog/ai-math/",
    },
    {
        "단계": "전체 복습",
        "자료": "AI반도체설계혁신특론 핵심 복습",
        "핵심": "머신러닝, 딥러닝, CNN, 생성모델, 온디바이스 경량화",
        "링크": "https://philipdekim-ond01.github.io/obsidian-blog/ai-semiconductor-course-review-ondevice-lightweighting.html",
    },
    {
        "단계": "Ondevice AI",
        "자료": "라즈베리파이로 배우는 전체 지도",
        "핵심": "TFLite, RPS, 전이학습, Quantization, Pruning",
        "링크": "https://philipdekim-ond01.github.io/obsidian-blog/ondevice-ai-00-overview.html",
    },
    {
        "단계": "경량화 실습",
        "자료": "OnDevice AI 경량화 강의자료 세션",
        "핵심": "Pruning, Clustering, PTQ, QAT, RPS 실습",
        "링크": "https://philipdekim-ond01.github.io/obsidian-blog/ondevice-ai-lightweighting-session.html",
    },
    {
        "단계": "QAT 코드",
        "자료": "RPS QAT 초보자용 코드",
        "핵심": "DenseNet121, 데이터 보강, QAT, TFLite 변환",
        "링크": "https://philipdekim-ond01.github.io/obsidian-blog/ondevice-ai-04-lightweighting-qat-beginner.html",
    },
    {
        "단계": "ResNet 비교",
        "자료": "ResNet RPS QAT 비교 실습",
        "핵심": "ResNet50, DenseNet121, QAT 결과 비교",
        "링크": "https://philipdekim-ond01.github.io/obsidian-blog/ondevice-ai-05-resnet-rps-qat.html",
    },
]

for row in blog_rows:
    left_col, right_col = st.columns([0.76, 0.24])
    with left_col:
        st.markdown(
            f"""
            <div class="resource-card" style="margin-bottom: 12px;">
                <h3>{row["단계"]} · {row["자료"]}</h3>
                <p>{row["핵심"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right_col:
        st.write("")
        st.write("")
        st.link_button("자료 열기", row["링크"], use_container_width=True)


st.markdown('<div class="section-title">학습 비중</div>', unsafe_allow_html=True)
weights = pd.DataFrame(
    {
        "영역": ["머신러닝", "딥러닝", "Ondevice AI"],
        "개념": [40, 35, 30],
        "실습": [35, 45, 50],
        "프로젝트": [25, 35, 45],
    }
)

fig = go.Figure()
for col, color in [("개념", "#2563eb"), ("실습", "#16a34a"), ("프로젝트", "#f97316")]:
    fig.add_trace(
        go.Bar(
            x=weights["영역"],
            y=weights[col],
            name=col,
            marker_color=color,
            text=weights[col],
            textposition="outside",
        )
    )

fig.update_layout(
    barmode="group",
    height=380,
    margin=dict(l=20, r=20, t=20, b=20),
    yaxis=dict(range=[0, 60], ticksuffix="%"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Noto Sans KR, sans-serif", size=14, color="#162033"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig, use_container_width=True)


st.markdown(
    """
    <div class="callout">
        한 문장으로 정리하면, 이 교육은 머신러닝으로 예측의 기본을 잡고,
        딥러닝으로 복잡한 데이터를 다루며, Ondevice AI로 실제 장치에서 쓸 수 있는 AI까지 연결하는 과정입니다.
    </div>
    """,
    unsafe_allow_html=True,
)

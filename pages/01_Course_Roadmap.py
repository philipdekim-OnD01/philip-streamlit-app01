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

    .week-rail-wrap {
        margin: 20px 0 28px;
        padding: 22px 18px;
        border-radius: 16px;
        border: 1px solid #dfe6f1;
        background: #ffffff;
        box-shadow: 0 12px 34px rgba(22, 32, 51, .06);
        overflow-x: auto;
    }

    .week-rail {
        min-width: 980px;
        display: grid;
        grid-template-columns: repeat(10, 1fr);
        align-items: start;
        position: relative;
        gap: 0;
    }

    .week-rail:before {
        content: "";
        position: absolute;
        top: 24px;
        left: 5%;
        right: 5%;
        height: 4px;
        border-radius: 999px;
        background: linear-gradient(90deg, #2563eb, #16a34a, #f97316);
        opacity: .24;
    }

    .week-node {
        position: relative;
        z-index: 1;
        display: grid;
        justify-items: center;
        gap: 8px;
        text-align: center;
        padding: 0 6px;
    }

    .week-dot {
        width: 52px;
        height: 52px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        background: #2563eb;
        border: 5px solid #eaf2ff;
        box-shadow: 0 10px 22px rgba(37, 99, 235, .18);
        font-weight: 800;
        font-size: 17px;
    }

    .week-node.ml .week-dot { background: #2563eb; }
    .week-node.dl .week-dot { background: #7c3aed; }
    .week-node.edge .week-dot { background: #16a34a; }
    .week-node.practice .week-dot { background: #f97316; }

    .week-label {
        min-height: 42px;
        color: #162033;
        font-size: 13px;
        font-weight: 800;
        line-height: 1.35;
    }

    .week-band {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 999px;
        background: #f0f6ff;
        color: #1d4ed8;
        font-size: 11px;
        font-weight: 800;
    }

    .week-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
    }

    .week-card {
        height: 100%;
        padding: 18px 20px;
        border-radius: 14px;
        border: 1px solid #dfe6f1;
        background: #ffffff;
        box-shadow: 0 10px 28px rgba(22, 32, 51, .055);
    }

    .week-card h3 {
        margin: 0 0 8px;
        color: #162033;
        font-size: 19px;
        font-weight: 800;
    }

    .week-card p {
        margin: 0 0 12px;
        color: #5b6475;
        font-size: 15px;
        line-height: 1.55;
    }

    .week-card a {
        display: inline-flex;
        align-items: center;
        padding: 8px 11px;
        border-radius: 9px;
        background: #edf4ff;
        color: #1d4ed8;
        font-size: 13px;
        font-weight: 800;
        text-decoration: none;
    }

    @media (max-width: 900px) {
        .week-grid {
            grid-template-columns: 1fr;
        }
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


st.markdown('<div class="section-title">10주 타임라인</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">1----2----3----4----5----6----7----8----9----10 흐름으로, 마지막 3주는 실습과 발표 중심입니다.</div>',
    unsafe_allow_html=True,
)

weeks = [
    {
        "week": "1",
        "band": "기초",
        "kind": "ml",
        "title": "선형대수와 AI",
        "body": "벡터, 행렬, `Xw`, 손실함수, 미분이 AI 모델 안에서 어떤 역할을 하는지 잡습니다.",
        "url": "https://philipdekim-ond01.github.io/obsidian-blog/ai-math/",
    },
    {
        "week": "2",
        "band": "ML",
        "kind": "ml",
        "title": "머신러닝 1",
        "body": "회귀, OLS, Ridge, Lasso, feature와 target의 관계를 이해합니다.",
        "url": "https://philipdekim-ond01.github.io/obsidian-blog/ai-semiconductor-course-review-ondevice-lightweighting.html",
    },
    {
        "week": "3",
        "band": "ML",
        "kind": "ml",
        "title": "머신러닝 2",
        "body": "분류, Naive Bayes, Decision Tree, SVM, accuracy/F1/ROC-AUC를 비교합니다.",
        "url": "https://philipdekim-ond01.github.io/obsidian-blog/ai-semiconductor-course-review-ondevice-lightweighting.html",
    },
    {
        "week": "4",
        "band": "DL",
        "kind": "dl",
        "title": "딥러닝 1",
        "body": "퍼셉트론, 활성화 함수, gradient descent, backpropagation의 기본 흐름을 봅니다.",
        "url": "https://philipdekim-ond01.github.io/obsidian-blog/ai-math/12-tiny-neural-network.html",
    },
    {
        "week": "5",
        "band": "DL",
        "kind": "dl",
        "title": "딥러닝 2",
        "body": "CNN, 이미지 분류, 데이터 증강, 전이학습을 On-device 실습의 준비 단계로 연결합니다.",
        "url": "https://philipdekim-ond01.github.io/obsidian-blog/ondevice-ai-02-transfer-learning.html",
    },
    {
        "week": "6",
        "band": "Edge",
        "kind": "edge",
        "title": "Ondevice AI 기본",
        "body": "라즈베리파이, 카메라 입력, TFLite 추론, confidence, FPS 관점을 정리합니다.",
        "url": "https://philipdekim-ond01.github.io/obsidian-blog/ondevice-ai-00-overview.html",
    },
    {
        "week": "7",
        "band": "Edge",
        "kind": "edge",
        "title": "모델 경량화",
        "body": "Quantization, Pruning, 모델 크기, latency, memory의 trade-off를 배웁니다.",
        "url": "https://philipdekim-ond01.github.io/obsidian-blog/ondevice-ai-03-lightweighting.html",
    },
    {
        "week": "8",
        "band": "실습 1",
        "kind": "practice",
        "title": "실습 1: TFLite RPS",
        "body": "가위바위보 분류 모델을 만들고 TFLite로 변환해 디바이스 추론 흐름을 확인합니다.",
        "url": "https://philipdekim-ond01.github.io/obsidian-blog/ondevice-ai-01-rps-tflite.html",
    },
    {
        "week": "9",
        "band": "실습 2",
        "kind": "practice",
        "title": "실습 2: QAT 경량화",
        "body": "DenseNet/ResNet 기반 RPS 모델에 데이터 보강과 QAT를 적용해 성능 손실을 줄입니다.",
        "url": "https://philipdekim-ond01.github.io/obsidian-blog/ondevice-ai-04-lightweighting-qat-beginner.html",
    },
    {
        "week": "10",
        "band": "발표",
        "kind": "practice",
        "title": "과제 발표",
        "body": "정확도, F1, 모델 크기, 추론 시간, 개선 아이디어를 한 장 리포트와 데모로 발표합니다.",
        "url": "https://philipdekim-ond01.github.io/obsidian-blog/ondevice-ai-05-resnet-rps-qat.html",
    },
]

rail_html = '<div class="week-rail-wrap"><div class="week-rail">'
for item in weeks:
    rail_html += f"""
    <div class="week-node {item["kind"]}">
        <div class="week-dot">{item["week"]}</div>
        <div class="week-label">{item["title"]}</div>
        <div class="week-band">{item["band"]}</div>
    </div>
    """
rail_html += "</div></div>"
st.markdown(rail_html, unsafe_allow_html=True)

st.markdown('<div class="week-grid">', unsafe_allow_html=True)
for item in weeks:
    st.markdown(
        f"""
        <div class="week-card">
            <h3>{item["week"]}주차 · {item["title"]}</h3>
            <p>{item["body"]}</p>
            <a href="{item["url"]}" target="_blank" rel="noopener">해당 강좌 열기</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)


left, right = st.columns([1.05, 0.95], gap="large")

with left:
    st.markdown('<div class="section-title">주차별 운영 포인트</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="code-box">1주차: 선형대수와 AI 계산 언어
2~3주차: 머신러닝 모델과 평가
4~5주차: 딥러닝과 CNN
6주차: Ondevice AI 기본 구조
7주차: 경량화와 성능 trade-off
8주차: 실습 1 - TFLite RPS
9주차: 실습 2 - QAT 경량화
10주차: 과제 발표 - 성능·속도·크기 비교</div>
        """,
        unsafe_allow_html=True,
    )

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

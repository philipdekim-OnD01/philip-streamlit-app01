import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="딥러닝 강의 로드맵",
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

    .roadmap-hero {
        padding: 42px 46px;
        border-radius: 18px;
        border: 1px solid #dbe6f7;
        background:
            radial-gradient(circle at 84% 20%, rgba(37, 99, 235, .18), transparent 28%),
            linear-gradient(135deg, #f8fbff 0%, #eef5ff 58%, #ffffff 100%);
        box-shadow: 0 18px 54px rgba(22, 32, 51, .08);
    }

    .roadmap-hero .label {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        background: #eaf2ff;
        color: #1d4ed8;
        font-size: 14px;
        font-weight: 800;
    }

    .roadmap-hero h1 {
        margin: 18px 0 12px;
        color: #162033;
        font-size: 50px;
        line-height: 1.12;
        font-weight: 800;
        letter-spacing: 0;
    }

    .roadmap-hero p {
        margin: 0;
        max-width: 850px;
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

    .phase-card,
    .lesson-card,
    .principle-card,
    .resource-card {
        height: 100%;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #dfe6f1;
        background: #ffffff;
        box-shadow: 0 12px 34px rgba(22, 32, 51, .06);
    }

    .phase-card {
        border-left: 6px solid #2563eb;
    }

    .phase-card .week {
        color: #2563eb;
        font-size: 14px;
        font-weight: 800;
    }

    .phase-card h3,
    .lesson-card h3,
    .principle-card h3,
    .resource-card h3 {
        margin: 8px 0 8px;
        color: #162033;
        font-size: 21px;
        font-weight: 800;
    }

    .phase-card p,
    .lesson-card p,
    .principle-card p,
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
    <section class="roadmap-hero">
        <div class="label">COURSE ROADMAP</div>
        <h1>딥러닝 강의 로드맵</h1>
        <p>
            머신러닝 기초 수학에서 시작해 지도학습, 모델 평가, Streamlit 배포,
            그리고 딥러닝 학습 루프와 Vision 이상탐지까지 이어지는 실습 중심 강의 흐름입니다.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="section-title">전체 학습 흐름</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">참고 폴더의 기초 수학, 지도학습, 평가, Streamlit 자료를 딥러닝 강의의 선수 지식으로 재배치했습니다.</div>',
    unsafe_allow_html=True,
)

phase_cols = st.columns(4)
phases = [
    (
        "Phase 1",
        "AI 수학과 회귀 기초",
        "`y - Xw`, OLS, Ridge, Lasso, 경사하강법을 통해 손실함수와 최적화의 감각을 만듭니다.",
        ["y-Xw", "OLS", "Regularization"],
    ),
    (
        "Phase 2",
        "지도학습 모델 비교",
        "Naive Bayes, Decision Tree, SVM을 비교하면서 모델마다 데이터를 나누는 방식이 다름을 이해합니다.",
        ["Bayes", "Tree", "SVM"],
    ),
    (
        "Phase 3",
        "딥러닝 학습 루프",
        "model, loader, criterion, optimizer, backward, step이 어떤 순서로 작동하는지 코드를 기준으로 설명합니다.",
        ["PyTorch", "Loss", "Backprop"],
    ),
    (
        "Phase 4",
        "Vision 응용과 배포",
        "CNN, 이상탐지, 성능지표를 연결하고 Streamlit으로 강의 결과물을 공유합니다.",
        ["CNN", "Anomaly", "Streamlit"],
    ),
]

for col, (week, title, body, tags) in zip(phase_cols, phases):
    with col:
        tag_html = "".join(f'<span class="tag">{tag}</span>' for tag in tags)
        st.markdown(
            f"""
            <div class="phase-card">
                <div class="week">{week}</div>
                <h3>{title}</h3>
                <p>{body}</p>
                <div class="tag-row">{tag_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


left, right = st.columns([1.05, 0.95], gap="large")

with left:
    st.markdown('<div class="section-title">12주 강의 설계</div>', unsafe_allow_html=True)
    timeline = [
        ("01", "실습 환경과 데이터", "Python, Jupyter, Streamlit, 데이터프레임, train/test split을 정리합니다."),
        ("02", "AI 수학 기초", "`y - Xw`, 오차, 손실함수, 미분, 행렬 계산을 선형회귀 기준으로 설명합니다."),
        ("03", "OLS, Ridge, Lasso", "오차제곱합, 정규화, 변수 선택, 과적합 완화를 비교합니다."),
        ("04", "분류 모델의 사고방식", "GNB, CategoricalNB, Decision Tree, SVM이 데이터를 어떻게 나누는지 비교합니다."),
        ("05", "평가 지표", "accuracy만 보지 않고 precision, recall, F1, ROC-AUC, PR-AUC를 함께 봅니다."),
        ("06", "딥러닝 기본 구조", "Tensor, batch, DNN, ReLU, CrossEntropyLoss, Adam optimizer를 연결합니다."),
        ("07", "학습 루프 해부", "forward, loss, zero_grad, backward, step을 한 줄씩 해석합니다."),
        ("08", "CNN Vision", "이미지 채널, convolution filter, feature map, pooling을 실습합니다."),
        ("09", "AutoEncoder와 이상탐지", "정상 데이터를 학습하고 reconstruction error로 이상 점수를 만듭니다."),
        ("10", "공정·의료 이미지 응용", "Casting, MVTec, 의료 영상 예제로 정상/불량 판별 흐름을 만듭니다."),
        ("11", "모델 개선 실험", "data augmentation, class imbalance, threshold tuning, recall 개선을 실험합니다."),
        ("12", "Streamlit 결과 공유", "학습 결과, 성능 리포트, 예측 데모를 Streamlit 앱으로 게시합니다."),
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
    st.markdown('<div class="section-title">핵심 코드는 이것입니다</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="code-box">def train_one_epoch(model, loader, criterion, optimizer):
    model.train()
    running = 0.0

    for x, y in loader:
        x, y = x.to(DEVICE), y.to(DEVICE)

        logit = model(x)             # 1. 예측
        loss = criterion(logit, y)   # 2. 오차 계산
        optimizer.zero_grad()        # 3. 이전 기울기 삭제
        loss.backward()              # 4. 역전파
        optimizer.step()             # 5. 가중치 갱신

        running += loss.item() * x.size(0)

    return running / len(loader.dataset)</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">초급자 설명 원칙</div>', unsafe_allow_html=True)
    principles = [
        ("수식보다 먼저 그림", "수식은 마지막에 정리하고, 먼저 데이터가 어떻게 이동하는지 보여줍니다."),
        ("모델보다 학습 루프", "DNN, CNN보다 먼저 forward, loss, backward, update 흐름을 잡습니다."),
        ("accuracy보다 목적", "불량 탐지에서는 accuracy보다 recall, F1, threshold가 더 중요할 수 있습니다."),
    ]
    for title, body in principles:
        st.markdown(
            f"""
            <div class="principle-card" style="margin-bottom: 14px;">
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
        "기초 수학",
        "`00.y - Xw`, 라그랑주, OLS 손실함수 자료",
        "딥러닝의 loss와 gradient를 이해하기 위한 선수 지식입니다.",
    ),
    (
        "지도학습",
        "Bayes, Tree, SVM, Ridge, Lasso, SVR 자료",
        "딥러닝과 전통 머신러닝 모델의 차이를 설명하는 비교 기준입니다.",
    ),
    (
        "서비스화",
        "Streamlit 기초와 머신러닝 서비스 자료",
        "강의 결과물을 웹 페이지로 공유하는 마지막 단계입니다.",
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


st.markdown('<div class="section-title">학습 난이도 곡선</div>', unsafe_allow_html=True)
difficulty = pd.DataFrame(
    {
        "주차": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        "난이도": [1.0, 1.8, 2.2, 2.5, 2.8, 3.4, 3.8, 4.2, 4.5, 4.6, 4.8, 4.0],
        "실습비중": [2.0, 1.5, 2.0, 2.6, 2.8, 3.5, 4.0, 4.3, 4.8, 4.8, 5.0, 4.5],
    }
)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=difficulty["주차"],
        y=difficulty["난이도"],
        mode="lines+markers",
        name="개념 난이도",
        line=dict(color="#2563eb", width=4),
    )
)
fig.add_trace(
    go.Scatter(
        x=difficulty["주차"],
        y=difficulty["실습비중"],
        mode="lines+markers",
        name="실습 비중",
        line=dict(color="#16a34a", width=4),
    )
)
fig.update_layout(
    height=380,
    margin=dict(l=20, r=20, t=20, b=20),
    yaxis=dict(range=[0, 5.4]),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Noto Sans KR, sans-serif", size=14, color="#162033"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig, use_container_width=True)


st.markdown(
    """
    <div class="callout">
        강의의 최종 목표는 모델 이름을 외우는 것이 아니라,
        데이터가 들어가서 예측이 나오고, 손실을 줄이는 방향으로 모델이 스스로 바뀌는 과정을 설명할 수 있게 만드는 것입니다.
    </div>
    """,
    unsafe_allow_html=True,
)

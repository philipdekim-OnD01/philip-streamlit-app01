from pathlib import Path
from datetime import datetime
import json

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import sklearn

from sklearn.model_selection import RandomizedSearchCV

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.linear_model import (
    LogisticRegression,
    LinearRegression,
    Ridge,
    Lasso,
)
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    r2_score,
    mean_absolute_error,
    mean_squared_error,
)
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor


st.set_page_config(
    page_title="Auto ML 모델 선택 예측 서비스",
    layout="wide"
)

SOURCE_REPO_URL = "https://github.com/philipdekim-OnD01/philip-streamlit-app01"
LIVE_HOME_URL = "https://philip-app-app01-kim.streamlit.app/"


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "saved_models"
REPORT_DIR = BASE_DIR / "reports"

MODEL_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)


def detect_problem_type(y: pd.Series) -> str:
    """
    타깃 컬럼의 성격을 보고 분류/회귀를 자동 판단한다.
    """
    if y.dtype == "object" or y.dtype.name == "category" or y.dtype == "bool":
        return "classification"

    unique_count = y.nunique()

    if pd.api.types.is_numeric_dtype(y) and unique_count <= 10:
        return "classification"

    return "regression"


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """
    숫자형 변수와 문자형 변수를 자동 분리해서 전처리한다.
    """
    numeric_features = X.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=["int64", "float64", "int32", "float32"]).columns.tolist()

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ],
        remainder="drop",
    )


def get_models(problem_type: str) -> dict:
    """
    문제 유형에 따라 회귀 모델 또는 분류 모델 후보를 반환한다.
    """
    if problem_type == "classification":
        return {
            "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
            "KNN": KNeighborsClassifier(),
            "Decision Tree": DecisionTreeClassifier(random_state=42),
            "Random Forest": RandomForestClassifier(random_state=42),
            "SVM": SVC(probability=True, random_state=42),
            "Gradient Boosting": GradientBoostingClassifier(random_state=42),
        }

    return {
        "Linear Regression": LinearRegression(),
        "Ridge": Ridge(random_state=42),
        "Lasso": Lasso(random_state=42),
        "KNN": KNeighborsRegressor(),
        "Decision Tree": DecisionTreeRegressor(random_state=42),
        "Random Forest": RandomForestRegressor(random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    }


def get_param_distributions(problem_type: str) -> dict:
    """
    RandomizedSearchCV에서 사용할 파라미터 후보.
    """
    if problem_type == "classification":
        return {
            "Logistic Regression": {"model__C": [0.01, 0.1, 1, 10, 100]},
            "KNN": {
                "model__n_neighbors": [3, 5, 7, 9, 11],
                "model__weights": ["uniform", "distance"],
                "model__p": [1, 2],
            },
            "Decision Tree": {
                "model__max_depth": [None, 3, 5, 7, 10],
                "model__min_samples_split": [2, 5, 10],
            },
            "Random Forest": {
                "model__n_estimators": [50, 100, 200],
                "model__max_depth": [None, 5, 10, 20],
                "model__min_samples_split": [2, 5, 10],
            },
            "SVM": {
                "model__C": [0.1, 1, 10],
                "model__gamma": ["scale", "auto"],
                "model__kernel": ["rbf", "linear"],
            },
            "Gradient Boosting": {
                "model__n_estimators": [50, 100, 200],
                "model__learning_rate": [0.01, 0.05, 0.1],
                "model__max_depth": [2, 3, 5],
            },
        }

    return {
        "Ridge": {"model__alpha": [0.01, 0.1, 1, 10, 100]},
        "Lasso": {"model__alpha": [0.001, 0.01, 0.1, 1, 10]},
        "KNN": {
            "model__n_neighbors": [3, 5, 7, 9, 11],
            "model__weights": ["uniform", "distance"],
            "model__p": [1, 2],
        },
        "Decision Tree": {
            "model__max_depth": [None, 3, 5, 7, 10],
            "model__min_samples_split": [2, 5, 10],
        },
        "Random Forest": {
            "model__n_estimators": [50, 100, 200],
            "model__max_depth": [None, 5, 10, 20],
            "model__min_samples_split": [2, 5, 10],
        },
        "Gradient Boosting": {
            "model__n_estimators": [50, 100, 200],
            "model__learning_rate": [0.01, 0.05, 0.1],
            "model__max_depth": [2, 3, 5],
        },
    }




def get_primary_metric_column(problem_type: str, df: pd.DataFrame) -> str | None:
    """Return the best available metric column for charts/sorting."""
    if df is None or len(df) == 0:
        return None
    preferred = ["f1", "accuracy", "precision", "recall"] if problem_type == "classification" else ["rmse", "r2", "mae"]
    for col in preferred:
        if col in df.columns:
            return col
    return None

def evaluate_model(problem_type: str, y_true, y_pred) -> dict:
    """
    회귀와 분류에 맞는 평가 지표를 계산한다.
    """
    if problem_type == "classification":
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, average="weighted", zero_division=0),
            "recall": recall_score(y_true, y_pred, average="weighted", zero_division=0),
            "f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
        }

    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    return {
        "r2": r2_score(y_true, y_pred),
        "mae": mean_absolute_error(y_true, y_pred),
        "rmse": rmse,
    }


def train_baseline_models(X_train, X_test, y_train, y_test, problem_type: str):
    """
    여러 모델을 기본 파라미터로 학습하고 성능을 비교한다.
    """
    preprocessor = build_preprocessor(X_train)
    models = get_models(problem_type)

    trained_models = {}
    results = []

    for model_name, model in models.items():
        pipe = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model),
            ]
        )

        try:
            pipe.fit(X_train, y_train)
            pred = pipe.predict(X_test)
            metrics = evaluate_model(problem_type, y_test, pred)

            trained_models[f"{model_name} 기본모델"] = {
                "model": pipe,
                "metrics": metrics,
                "best_params": None,
                "model_type": "baseline",
                "base_model_name": model_name,
            }

            row = {
                "model_name": f"{model_name} 기본모델",
                "base_model_name": model_name,
                "model_type": "baseline",
            }
            row.update(metrics)
            results.append(row)
        except Exception as exc:
            st.warning(f"{model_name} 학습 실패: {exc}")

    result_df = pd.DataFrame(results)

    metric_col = get_primary_metric_column(problem_type, result_df)
    if metric_col is not None:
        ascending = metric_col in {"rmse", "mae"}
        result_df = result_df.sort_values(metric_col, ascending=ascending)

    return trained_models, result_df


def tune_top_models(
    trained_models: dict,
    baseline_result_df: pd.DataFrame,
    X_train,
    X_test,
    y_train,
    y_test,
    problem_type: str,
    top_n: int,
    n_iter: int,
):
    """
    기본 모델 성능 상위 top_n개만 RandomizedSearchCV로 튜닝한다.
    """
    param_distributions = get_param_distributions(problem_type)
    tuned_models = {}
    tuned_results = []
    top_models = baseline_result_df.head(top_n)

    scoring = "f1_weighted" if problem_type == "classification" else "neg_root_mean_squared_error"

    for _, row in top_models.iterrows():
        base_model_name = row["base_model_name"]
        baseline_key = row["model_name"]

        if base_model_name not in param_distributions:
            st.info(f"{base_model_name}은 튜닝 파라미터가 없어 건너뜁니다.")
            continue

        baseline_model = trained_models[baseline_key]["model"]
        params = param_distributions[base_model_name]

        search = RandomizedSearchCV(
            estimator=baseline_model,
            param_distributions=params,
            n_iter=n_iter,
            scoring=scoring,
            cv=3,
            random_state=42,
            n_jobs=-1,
            error_score="raise",
        )

        try:
            search.fit(X_train, y_train)
            best_model = search.best_estimator_
            pred = best_model.predict(X_test)
            metrics = evaluate_model(problem_type, y_test, pred)

            tuned_key = f"{base_model_name} 튜닝모델"
            tuned_models[tuned_key] = {
                "model": best_model,
                "metrics": metrics,
                "best_params": search.best_params_,
                "best_cv_score": search.best_score_,
                "model_type": "tuned",
                "base_model_name": base_model_name,
            }

            result_row = {
                "model_name": tuned_key,
                "base_model_name": base_model_name,
                "model_type": "tuned",
                "best_cv_score": search.best_score_,
                "best_params": search.best_params_,
            }
            result_row.update(metrics)
            tuned_results.append(result_row)
        except Exception as exc:
            st.warning(f"{base_model_name} 튜닝 실패: {exc}")

    tuned_result_df = pd.DataFrame(tuned_results)

    if len(tuned_result_df) > 0:
        metric_col = get_primary_metric_column(problem_type, tuned_result_df)
        if metric_col is not None:
            ascending = metric_col in {"rmse", "mae"}
            tuned_result_df = tuned_result_df.sort_values(metric_col, ascending=ascending)

    return tuned_models, tuned_result_df


def save_model_artifacts(
    selected_model_name: str,
    selected_payload: dict,
    problem_type: str,
    target_column: str,
    feature_columns: list,
    metrics: dict,
    train_report_df: pd.DataFrame,
    test_size: float,
):
    """
    선택한 모델과 관련 정보를 저장한다.
    """
    model_path = MODEL_DIR / "selected_model.joblib"
    info_path = MODEL_DIR / "model_info.json"
    feature_path = MODEL_DIR / "feature_columns.json"
    report_path = REPORT_DIR / "training_report.csv"

    payload = {
        "model_name": selected_model_name,
        "model": selected_payload["model"],
        "problem_type": problem_type,
        "target_column": target_column,
        "feature_columns": feature_columns,
        "metrics": metrics,
        "best_params": selected_payload.get("best_params"),
        "sklearn_version": sklearn.__version__,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    joblib.dump(payload, model_path)

    model_info = {
        "problem_type": problem_type,
        "target_column": target_column,
        "selected_model_name": selected_model_name,
        "metrics": metrics,
        "best_params": selected_payload.get("best_params"),
        "test_size": test_size,
        "feature_columns": feature_columns,
        "sklearn_version": sklearn.__version__,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(model_info, f, ensure_ascii=False, indent=4)

    with open(feature_path, "w", encoding="utf-8") as f:
        json.dump(feature_columns, f, ensure_ascii=False, indent=4)

    train_report_df.to_csv(report_path, index=False, encoding="utf-8-sig")

    return model_path, info_path, feature_path, report_path


def make_prediction_input_ui(X: pd.DataFrame) -> pd.DataFrame:
    """
    사용자가 화면에서 직접 예측값을 입력하는 UI.
    """
    input_data = {}
    for col in X.columns:
        if pd.api.types.is_numeric_dtype(X[col]):
            col_min = float(X[col].min())
            col_max = float(X[col].max())
            default_value = float(X[col].median())
            input_data[col] = st.number_input(
                f"{col}",
                min_value=col_min,
                max_value=col_max,
                value=default_value,
            )
        else:
            options = X[col].dropna().astype(str).unique().tolist()
            if len(options) == 0:
                options = [""]
            input_data[col] = st.selectbox(f"{col}", options)

    return pd.DataFrame([input_data])

def get_param_grid_for_selected_model(problem_type: str, base_model_name: str) -> dict:
    """
    사용자가 선택한 모델 하나에 대해서만 파라미터 튜닝 후보를 반환한다.
    Pipeline 안의 모델 단계 이름이 'model'이므로 파라미터 앞에 model__을 붙인다.
    """

    if problem_type == "classification":
        grids = {
            "Logistic Regression": {
                "model__C": [0.01, 0.1, 1, 10, 100],
            },
            "KNN": {
                "model__n_neighbors": [3, 5, 7, 9, 11, 15],
                "model__weights": ["uniform", "distance"],
                "model__p": [1, 2],
            },
            "Decision Tree": {
                "model__max_depth": [None, 3, 5, 7, 10],
                "model__min_samples_split": [2, 5, 10],
                "model__min_samples_leaf": [1, 2, 4],
            },
            "Random Forest": {
                "model__n_estimators": [50, 100, 200, 300],
                "model__max_depth": [None, 5, 10, 20],
                "model__min_samples_split": [2, 5, 10],
                "model__min_samples_leaf": [1, 2, 4],
            },
            "SVM": {
                "model__C": [0.1, 1, 10, 100],
                "model__gamma": ["scale", "auto"],
                "model__kernel": ["rbf", "linear"],
            },
            "Gradient Boosting": {
                "model__n_estimators": [50, 100, 200],
                "model__learning_rate": [0.01, 0.05, 0.1],
                "model__max_depth": [2, 3, 5],
            },
        }

    else:
        grids = {
            "Linear Regression": {},
            "Ridge": {
                "model__alpha": [0.01, 0.1, 1, 10, 100],
            },
            "Lasso": {
                "model__alpha": [0.001, 0.01, 0.1, 1, 10],
            },
            "KNN": {
                "model__n_neighbors": [3, 5, 7, 9, 11, 15],
                "model__weights": ["uniform", "distance"],
                "model__p": [1, 2],
            },
            "Decision Tree": {
                "model__max_depth": [None, 3, 5, 7, 10],
                "model__min_samples_split": [2, 5, 10],
                "model__min_samples_leaf": [1, 2, 4],
            },
            "Random Forest": {
                "model__n_estimators": [50, 100, 200, 300],
                "model__max_depth": [None, 5, 10, 20],
                "model__min_samples_split": [2, 5, 10],
                "model__min_samples_leaf": [1, 2, 4],
            },
            "Gradient Boosting": {
                "model__n_estimators": [50, 100, 200],
                "model__learning_rate": [0.01, 0.05, 0.1],
                "model__max_depth": [2, 3, 5],
            },
        }

    return grids.get(base_model_name, {})

def tune_selected_model(
    selected_model_name: str,
    selected_payload: dict,
    X_train,
    X_test,
    y_train,
    y_test,
    problem_type: str,
    n_iter: int = 10,
    cv: int = 3,
):
    """
    사용자가 선택한 모델 하나만 파라미터 튜닝한다.
    튜닝 전 성능과 튜닝 후 성능을 비교할 수 있도록 결과를 반환한다.
    """

    base_model_name = selected_payload["base_model_name"]
    baseline_model = selected_payload["model"]
    baseline_metrics = selected_payload["metrics"]

    param_grid = get_param_grid_for_selected_model(problem_type, base_model_name)

    if not param_grid:
        raise ValueError(f"{base_model_name}은 튜닝할 파라미터가 없습니다.")

    if problem_type == "classification":
        scoring = "f1_weighted"
    else:
        scoring = "neg_root_mean_squared_error"

    search = RandomizedSearchCV(
        estimator=baseline_model,
        param_distributions=param_grid,
        n_iter=n_iter,
        scoring=scoring,
        cv=cv,
        random_state=42,
        n_jobs=-1,
        error_score="raise",
    )

    search.fit(X_train, y_train)

    tuned_model = search.best_estimator_
    tuned_pred = tuned_model.predict(X_test)
    tuned_metrics = evaluate_model(problem_type, y_test, tuned_pred)

    tuned_model_name = f"{base_model_name} 튜닝모델"

    tuned_payload = {
        "model": tuned_model,
        "metrics": tuned_metrics,
        "best_params": search.best_params_,
        "best_cv_score": search.best_score_,
        "model_type": "tuned",
        "base_model_name": base_model_name,
    }

    before_row = {
        "model_name": selected_model_name,
        "base_model_name": base_model_name,
        "model_type": "before_tuning",
    }
    before_row.update(baseline_metrics)

    after_row = {
        "model_name": tuned_model_name,
        "base_model_name": base_model_name,
        "model_type": "after_tuning",
        "best_cv_score": search.best_score_,
        "best_params": search.best_params_,
    }
    after_row.update(tuned_metrics)

    compare_df = pd.DataFrame([before_row, after_row])

    metric_col = get_primary_metric_column(problem_type, compare_df)
    if metric_col is not None:
        ascending = metric_col in {"rmse", "mae"}
        compare_df = compare_df.sort_values(metric_col, ascending=ascending)

    return tuned_model_name, tuned_payload, compare_df

def detect_problem_type(y: pd.Series) -> str:
    """
    타깃 컬럼의 성격을 보고 분류/회귀를 자동 판단한다.
    단, Streamlit 화면에서 사용자가 직접 수정할 수 있게 한다.
    """
    if y.dtype == "object" or y.dtype.name == "category" or y.dtype == "bool":
        return "classification"

    unique_count = y.nunique()

    if pd.api.types.is_numeric_dtype(y) and unique_count <= 10:
        return "classification"

    return "regression"


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """
    숫자형 변수와 문자형 변수를 자동 분리해서 전처리한다.
    숫자형: 결측치 중앙값 처리 + 표준화
    문자형: 결측치 최빈값 처리 + 원핫인코딩
    """
    numeric_features = X.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=["int64", "float64", "int32", "float32"]).columns.tolist()

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ],
        remainder="drop",
    )

    return preprocessor


def get_models(problem_type: str) -> dict:
    """
    문제 유형에 따라 회귀 모델 또는 분류 모델 후보를 반환한다.
    """
    if problem_type == "classification":
        return {
            "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
            "KNN": KNeighborsClassifier(),
            "Decision Tree": DecisionTreeClassifier(random_state=42),
            "Random Forest": RandomForestClassifier(random_state=42),
            "SVM": SVC(probability=True, random_state=42),
            "Gradient Boosting": GradientBoostingClassifier(random_state=42),
        }

    return {
        "Linear Regression": LinearRegression(),
        "Ridge": Ridge(random_state=42),
        "Lasso": Lasso(random_state=42),
        "KNN": KNeighborsRegressor(),
        "Decision Tree": DecisionTreeRegressor(random_state=42),
        "Random Forest": RandomForestRegressor(random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    }


def get_param_distributions(problem_type: str) -> dict:
    """
    RandomizedSearchCV에서 사용할 파라미터 후보.
    Pipeline 안에서 모델 이름을 'model'로 지정했으므로 파라미터 앞에 model__을 붙인다.
    """
    if problem_type == "classification":
        return {
            "Logistic Regression": {
                "model__C": [0.01, 0.1, 1, 10, 100],
            },
            "KNN": {
                "model__n_neighbors": [3, 5, 7, 9, 11],
                "model__weights": ["uniform", "distance"],
                "model__p": [1, 2],
            },
            "Decision Tree": {
                "model__max_depth": [None, 3, 5, 7, 10],
                "model__min_samples_split": [2, 5, 10],
            },
            "Random Forest": {
                "model__n_estimators": [50, 100, 200],
                "model__max_depth": [None, 5, 10, 20],
                "model__min_samples_split": [2, 5, 10],
            },
            "SVM": {
                "model__C": [0.1, 1, 10],
                "model__gamma": ["scale", "auto"],
                "model__kernel": ["rbf", "linear"],
            },
            "Gradient Boosting": {
                "model__n_estimators": [50, 100, 200],
                "model__learning_rate": [0.01, 0.05, 0.1],
                "model__max_depth": [2, 3, 5],
            },
        }

    return {
        "Ridge": {
            "model__alpha": [0.01, 0.1, 1, 10, 100],
        },
        "Lasso": {
            "model__alpha": [0.001, 0.01, 0.1, 1, 10],
        },
        "KNN": {
            "model__n_neighbors": [3, 5, 7, 9, 11],
            "model__weights": ["uniform", "distance"],
            "model__p": [1, 2],
        },
        "Decision Tree": {
            "model__max_depth": [None, 3, 5, 7, 10],
            "model__min_samples_split": [2, 5, 10],
        },
        "Random Forest": {
            "model__n_estimators": [50, 100, 200],
            "model__max_depth": [None, 5, 10, 20],
            "model__min_samples_split": [2, 5, 10],
        },
        "Gradient Boosting": {
            "model__n_estimators": [50, 100, 200],
            "model__learning_rate": [0.01, 0.05, 0.1],
            "model__max_depth": [2, 3, 5],
        },
    }




def get_primary_metric_column(problem_type: str, df: pd.DataFrame) -> str | None:
    """Return the best available metric column for charts/sorting."""
    if df is None or len(df) == 0:
        return None
    preferred = ["f1", "accuracy", "precision", "recall"] if problem_type == "classification" else ["rmse", "r2", "mae"]
    for col in preferred:
        if col in df.columns:
            return col
    return None

def evaluate_model(problem_type: str, y_true, y_pred) -> dict:
    """
    회귀와 분류에 맞는 평가 지표를 계산한다.
    """
    if problem_type == "classification":
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, average="weighted", zero_division=0),
            "recall": recall_score(y_true, y_pred, average="weighted", zero_division=0),
            "f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
        }

    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)

    return {
        "r2": r2_score(y_true, y_pred),
        "mae": mean_absolute_error(y_true, y_pred),
        "rmse": rmse,
    }


def train_baseline_models(X_train, X_test, y_train, y_test, problem_type: str):
    """
    여러 모델을 기본 파라미터로 학습하고 성능을 비교한다.
    """
    preprocessor = build_preprocessor(X_train)
    models = get_models(problem_type)

    trained_models = {}
    results = []

    for model_name, model in models.items():
        pipe = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model),
            ]
        )

        try:
            pipe.fit(X_train, y_train)
            pred = pipe.predict(X_test)
            metrics = evaluate_model(problem_type, y_test, pred)

            trained_models[f"{model_name} 기본모델"] = {
                "model": pipe,
                "metrics": metrics,
                "best_params": None,
                "model_type": "baseline",
                "base_model_name": model_name,
            }

            row = {
                "model_name": f"{model_name} 기본모델",
                "base_model_name": model_name,
                "model_type": "baseline",
            }
            row.update(metrics)
            results.append(row)

        except Exception as exc:
            st.warning(f"{model_name} 학습 실패: {exc}")

    result_df = pd.DataFrame(results)

    metric_col = get_primary_metric_column(problem_type, result_df)
    if metric_col is not None:
        ascending = metric_col in {"rmse", "mae"}
        result_df = result_df.sort_values(metric_col, ascending=ascending)

    return trained_models, result_df


def tune_top_models(
    trained_models: dict,
    baseline_result_df: pd.DataFrame,
    X_train,
    X_test,
    y_train,
    y_test,
    problem_type: str,
    top_n: int,
    n_iter: int,
):
    """
    기본 모델 성능 상위 top_n개만 RandomizedSearchCV로 튜닝한다.
    """
    param_distributions = get_param_distributions(problem_type)
    tuned_models = {}
    tuned_results = []

    top_models = baseline_result_df.head(top_n)

    if problem_type == "classification":
        scoring = "f1_weighted"
    else:
        scoring = "neg_root_mean_squared_error"

    for _, row in top_models.iterrows():
        base_model_name = row["base_model_name"]
        baseline_key = row["model_name"]

        if base_model_name not in param_distributions:
            st.info(f"{base_model_name}은 튜닝 파라미터가 없어 건너뜁니다.")
            continue

        baseline_model = trained_models[baseline_key]["model"]
        params = param_distributions[base_model_name]

        search = RandomizedSearchCV(
            estimator=baseline_model,
            param_distributions=params,
            n_iter=n_iter,
            scoring=scoring,
            cv=3,
            random_state=42,
            n_jobs=-1,
            error_score="raise",
        )

        try:
            search.fit(X_train, y_train)

            best_model = search.best_estimator_
            pred = best_model.predict(X_test)
            metrics = evaluate_model(problem_type, y_test, pred)

            tuned_key = f"{base_model_name} 튜닝모델"

            tuned_models[tuned_key] = {
                "model": best_model,
                "metrics": metrics,
                "best_params": search.best_params_,
                "best_cv_score": search.best_score_,
                "model_type": "tuned",
                "base_model_name": base_model_name,
            }

            result_row = {
                "model_name": tuned_key,
                "base_model_name": base_model_name,
                "model_type": "tuned",
                "best_cv_score": search.best_score_,
                "best_params": search.best_params_,
            }
            result_row.update(metrics)
            tuned_results.append(result_row)

        except Exception as exc:
            st.warning(f"{base_model_name} 튜닝 실패: {exc}")

    tuned_result_df = pd.DataFrame(tuned_results)

    if len(tuned_result_df) > 0:
        metric_col = get_primary_metric_column(problem_type, tuned_result_df)
        if metric_col is not None:
            ascending = metric_col in {"rmse", "mae"}
            tuned_result_df = tuned_result_df.sort_values(metric_col, ascending=ascending)

    return tuned_models, tuned_result_df


def save_model_artifacts(
    selected_model_name: str,
    selected_payload: dict,
    problem_type: str,
    target_column: str,
    feature_columns: list,
    metrics: dict,
    train_report_df: pd.DataFrame,
    test_size: float,
):
    """
    선택한 모델과 관련 정보를 저장한다.
    """
    model_path = MODEL_DIR / "selected_model.joblib"
    info_path = MODEL_DIR / "model_info.json"
    feature_path = MODEL_DIR / "feature_columns.json"
    report_path = REPORT_DIR / "training_report.csv"

    payload = {
        "model_name": selected_model_name,
        "model": selected_payload["model"],
        "problem_type": problem_type,
        "target_column": target_column,
        "feature_columns": feature_columns,
        "metrics": metrics,
        "best_params": selected_payload.get("best_params"),
        "sklearn_version": sklearn.__version__,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    joblib.dump(payload, model_path)

    model_info = {
        "problem_type": problem_type,
        "target_column": target_column,
        "selected_model_name": selected_model_name,
        "metrics": metrics,
        "best_params": selected_payload.get("best_params"),
        "test_size": test_size,
        "feature_columns": feature_columns,
        "sklearn_version": sklearn.__version__,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(model_info, f, ensure_ascii=False, indent=4)

    with open(feature_path, "w", encoding="utf-8") as f:
        json.dump(feature_columns, f, ensure_ascii=False, indent=4)

    train_report_df.to_csv(report_path, index=False, encoding="utf-8-sig")

    return model_path, info_path, feature_path, report_path


def make_prediction_input_ui(X: pd.DataFrame) -> pd.DataFrame:
    """
    사용자가 화면에서 직접 예측값을 입력하는 UI.
    """
    input_data = {}

    for col in X.columns:
        if pd.api.types.is_numeric_dtype(X[col]):
            default_value = float(X[col].median()) if X[col].notna().sum() > 0 else 0.0
            input_data[col] = st.number_input(col, value=default_value)
        else:
            values = X[col].dropna().unique().tolist()
            if len(values) > 0 and len(values) <= 30:
                input_data[col] = st.selectbox(col, values)
            else:
                input_data[col] = st.text_input(col, value=str(values[0]) if len(values) > 0 else "")

    return pd.DataFrame([input_data])


def get_feature_importance(model_pipeline, X: pd.DataFrame):
    """
    feature importance를 가져온다.
    트리 기반 모델에서만 안정적으로 가능하다.
    원핫인코딩 후 변수명이 늘어나므로 get_feature_names_out을 사용한다.
    """
    try:
        model = model_pipeline.named_steps["model"]
        preprocessor = model_pipeline.named_steps["preprocessor"]

        if not hasattr(model, "feature_importances_"):
            return None

        feature_names = preprocessor.get_feature_names_out()
        importances = model.feature_importances_

        importance_df = pd.DataFrame(
            {
                "feature": feature_names,
                "importance": importances,
            }
        ).sort_values("importance", ascending=False)

        return importance_df

    except Exception:
        return None


st.title("Auto ML 지도학습 모델 선택 · 튜닝 · 저장 · 예측 앱")

st.markdown(
    """
    이 앱은 CSV 데이터를 업로드한 뒤 타깃 컬럼을 선택하면, 데이터 성격에 맞게 분류 또는 회귀 모델을 학습합니다.
    먼저 여러 모델을 기본 파라미터로 비교하고, 그다음 상위 모델만 파라미터 튜닝하여 최종 모델을 선택할 수 있습니다.
    """
)

link_col1, link_col2 = st.columns(2)
with link_col1:
    st.link_button("메인 홈으로", LIVE_HOME_URL, use_container_width=True)
with link_col2:
    st.link_button("GitHub 소스", SOURCE_REPO_URL, use_container_width=True)


with st.sidebar:
    st.header("설정")
    st.caption("메인 홈과 소스 저장소 연결")
    st.link_button("메인 홈 열기", LIVE_HOME_URL)
    st.link_button("GitHub 저장소 열기", SOURCE_REPO_URL)
    st.divider()

    uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

    test_size = st.slider(
        "테스트 데이터 비율",
        min_value=0.1,
        max_value=0.4,
        value=0.2,
        step=0.05,
    )

    run_tuning = st.checkbox("상위 모델 파라미터 튜닝 실행", value=True)

    top_n = st.slider(
        "튜닝할 상위 모델 개수",
        min_value=1,
        max_value=3,
        value=2,
        step=1,
    )

    n_iter = st.slider(
        "튜닝 탐색 횟수 n_iter",
        min_value=5,
        max_value=30,
        value=10,
        step=5,
    )

    st.divider()
    train_button = st.button("모델 학습 실행", type="primary", width="stretch")


if uploaded_file is None:
    st.info("왼쪽 사이드바에서 CSV 파일을 업로드하세요.")
    st.stop()


df = pd.read_csv(uploaded_file)

tab_data, tab_train, tab_tune, tab_viz, tab_predict, tab_save = st.tabs(
    [
        "1. 데이터 확인",
        "2. 기본 모델 비교",
        "3. 튜닝 결과",
        "4. 시각화",
        "5. 예측 실행",
        "6. 모델 저장",
    ]
)


with tab_data:
    st.subheader("데이터 미리보기")
    st.dataframe(df.head(), width="stretch")

    st.subheader("데이터 기본 정보")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("행 수", df.shape[0])
    col2.metric("열 수", df.shape[1])
    col3.metric("결측치 수", int(df.isna().sum().sum()))
    col4.metric("숫자형 컬럼 수", len(df.select_dtypes(include=np.number).columns))
    col5.metric("문자형 컬럼 수", len(df.select_dtypes(exclude=np.number).columns))

    st.subheader("컬럼별 결측치")
    missing_df = df.isna().sum().reset_index()
    missing_df.columns = ["column", "missing_count"]
    st.dataframe(missing_df, width="stretch")

    target_column = st.selectbox("예측할 타깃 컬럼을 선택하세요.", df.columns)

    exclude_columns = st.multiselect(
        "학습에서 제외할 컬럼을 선택하세요.",
        [col for col in df.columns if col != target_column],
    )

    y_raw = df[target_column]
    detected_type = detect_problem_type(y_raw)

    problem_type = st.radio(
        "문제 유형",
        ["classification", "regression"],
        index=0 if detected_type == "classification" else 1,
        horizontal=True,
    )

    st.info(f"자동 판단 결과: {detected_type} / 현재 선택: {problem_type}")

    st.session_state["target_column"] = target_column
    st.session_state["exclude_columns"] = exclude_columns
    st.session_state["problem_type"] = problem_type


target_column = st.session_state.get("target_column")
exclude_columns = st.session_state.get("exclude_columns", [])
problem_type = st.session_state.get("problem_type")


if target_column is None or problem_type is None:
    st.stop()


if train_button:
    work_df = df.copy()

    if work_df[target_column].isna().sum() > 0:
        st.warning("타깃 컬럼에 결측치가 있어 해당 행을 제거합니다.")
        work_df = work_df.dropna(subset=[target_column])

    if work_df.shape[0] < 20:
        st.error("데이터 행 수가 너무 적습니다. 최소 20행 이상을 권장합니다.")
        st.stop()

    feature_columns = [
        col for col in work_df.columns
        if col != target_column and col not in exclude_columns
    ]

    if len(feature_columns) < 1:
        st.error("학습에 사용할 feature 컬럼이 없습니다.")
        st.stop()

    X = work_df[feature_columns]
    y = work_df[target_column]

    label_encoder = None

    if problem_type == "classification":
        if y.nunique() < 2:
            st.error("분류 문제에서 클래스가 1개뿐입니다. 학습할 수 없습니다.")
            st.stop()

        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y.astype(str))

        stratify_option = y if len(np.unique(y)) > 1 else None
    else:
        if not pd.api.types.is_numeric_dtype(y):
            st.error("회귀 문제의 타깃 컬럼은 숫자형이어야 합니다.")
            st.stop()

        stratify_option = None

    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=42,
            stratify=stratify_option if problem_type == "classification" else None,
        )
    except Exception:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=42,
        )

    with st.spinner("기본 모델을 학습하는 중입니다..."):
        trained_models, baseline_result_df = train_baseline_models(
            X_train,
            X_test,
            y_train,
            y_test,
            problem_type,
        )

    all_models = trained_models.copy()
    all_result_df = baseline_result_df.copy()
    tuned_result_df = pd.DataFrame()

    if run_tuning:
        with st.spinner("상위 모델만 파라미터 튜닝하는 중입니다..."):
            tuned_models, tuned_result_df = tune_top_models(
                trained_models,
                baseline_result_df,
                X_train,
                X_test,
                y_train,
                y_test,
                problem_type,
                top_n,
                n_iter,
            )

        all_models.update(tuned_models)

        if len(tuned_result_df) > 0:
            all_result_df = pd.concat([baseline_result_df, tuned_result_df], ignore_index=True)

            if problem_type == "classification":
                all_result_df = all_result_df.sort_values("f1", ascending=False)
            else:
                all_result_df = all_result_df.sort_values("rmse", ascending=True)

    st.session_state["X"] = X
    st.session_state["y"] = y
    st.session_state["X_test"] = X_test
    st.session_state["y_test"] = y_test
    st.session_state["problem_type"] = problem_type
    st.session_state["target_column"] = target_column
    st.session_state["feature_columns"] = feature_columns
    st.session_state["label_encoder"] = label_encoder
    st.session_state["trained_models"] = all_models
    st.session_state["baseline_result_df"] = baseline_result_df
    st.session_state["tuned_result_df"] = tuned_result_df
    st.session_state["all_result_df"] = all_result_df
    st.session_state["test_size"] = test_size

    st.success("모델 학습이 완료되었습니다.")


with tab_train:
    st.subheader("기본 모델 성능 비교")

    if "baseline_result_df" not in st.session_state:
        st.info("사이드바에서 모델 학습 실행 버튼을 누르세요.")
    else:
        baseline_result_df = st.session_state["baseline_result_df"]
        st.dataframe(baseline_result_df, width="stretch")

        metric_col = get_primary_metric_column(st.session_state["problem_type"], baseline_result_df)
        if metric_col is None:
            st.warning("표시할 평가 지표가 없습니다. 먼저 모델 학습이 정상적으로 완료되었는지 확인하세요.")
        else:
            st.bar_chart(baseline_result_df.set_index("model_name")[metric_col])


with tab_tune:
    st.subheader("파라미터 튜닝 결과")

    if "tuned_result_df" not in st.session_state:
        st.info("아직 튜닝 결과가 없습니다.")
    else:
        tuned_result_df = st.session_state["tuned_result_df"]

        if len(tuned_result_df) == 0:
            st.warning("튜닝된 모델이 없습니다. Linear Regression처럼 튜닝 파라미터가 없는 모델은 제외됩니다.")
        else:
            st.dataframe(tuned_result_df, width="stretch")

            st.subheader("기본 모델 + 튜닝 모델 전체 비교")
            st.dataframe(st.session_state["all_result_df"], width="stretch")


with tab_viz:
    st.subheader("선택 모델 시각화")

    if "trained_models" not in st.session_state:
        st.info("먼저 모델을 학습하세요.")
    else:
        all_models = st.session_state["trained_models"]
        selected_for_viz = st.selectbox(
            "시각화할 모델 선택",
            list(all_models.keys()),
            key="viz_model",
        )

        model = all_models[selected_for_viz]["model"]
        X_test = st.session_state["X_test"]
        y_test = st.session_state["y_test"]
        problem_type = st.session_state["problem_type"]

        pred = model.predict(X_test)

        if problem_type == "classification":
            st.subheader("Confusion Matrix")
            cm = confusion_matrix(y_test, pred)
            st.dataframe(pd.DataFrame(cm), width="stretch")

            st.subheader("Classification Report")
            report = classification_report(y_test, pred, output_dict=True, zero_division=0)
            st.dataframe(pd.DataFrame(report).transpose(), width="stretch")

        else:
            st.subheader("실제값 vs 예측값")
            plot_df = pd.DataFrame(
                {
                    "actual": y_test,
                    "predicted": pred,
                }
            )
            st.scatter_chart(plot_df, x="actual", y="predicted")

            st.subheader("잔차 분포")
            residual_df = pd.DataFrame(
                {
                    "residual": y_test - pred,
                }
            )
            st.bar_chart(residual_df["residual"])

        importance_df = get_feature_importance(model, st.session_state["X"])

        if importance_df is not None:
            st.subheader("Feature Importance")
            st.dataframe(importance_df.head(30), width="stretch")
            st.bar_chart(importance_df.head(20).set_index("feature")["importance"])
        else:
            st.info("이 모델은 feature importance를 직접 제공하지 않습니다.")


with tab_predict:
    st.subheader("새로운 입력값으로 예측하기")

    if "trained_models" not in st.session_state:
        st.info("먼저 모델을 학습하세요.")
    else:
        all_models = st.session_state["trained_models"]
        selected_model_name = st.selectbox(
            "예측에 사용할 모델 선택",
            list(all_models.keys()),
            key="predict_model",
        )

        selected_model = all_models[selected_model_name]["model"]
        X = st.session_state["X"]

        st.markdown("아래 값을 입력한 뒤 예측 버튼을 누르세요.")
        input_df = make_prediction_input_ui(X)

        if st.button("단일 예측 실행", type="primary"):
            pred = selected_model.predict(input_df)

            problem_type = st.session_state["problem_type"]
            label_encoder = st.session_state.get("label_encoder")

            if problem_type == "classification" and label_encoder is not None:
                pred_label = label_encoder.inverse_transform(pred)[0]
                st.success(f"예측 결과: {pred_label}")
            else:
                st.success(f"예측 결과: {pred[0]}")

        st.divider()
        st.subheader("예측용 CSV 배치 예측")

        batch_file = st.file_uploader("예측용 CSV 업로드", type=["csv"], key="batch_csv")

        if batch_file is not None:
            batch_df = pd.read_csv(batch_file)
            required_features = st.session_state["feature_columns"]

            missing = [col for col in required_features if col not in batch_df.columns]
            extra = [col for col in batch_df.columns if col not in required_features]

            if missing:
                st.error(f"예측 데이터에 부족한 컬럼이 있습니다: {missing}")
            else:
                if extra:
                    st.warning(f"학습에 사용하지 않은 추가 컬럼은 무시됩니다: {extra}")

                pred_input = batch_df[required_features]
                batch_pred = selected_model.predict(pred_input)

                result_df = batch_df.copy()

                if st.session_state["problem_type"] == "classification" and st.session_state.get("label_encoder") is not None:
                    result_df["prediction"] = st.session_state["label_encoder"].inverse_transform(batch_pred)
                else:
                    result_df["prediction"] = batch_pred

                st.dataframe(result_df.head(30), width="stretch")

                csv = result_df.to_csv(index=False).encode("utf-8-sig")

                st.download_button(
                    label="예측 결과 CSV 다운로드",
                    data=csv,
                    file_name="prediction_result.csv",
                    mime="text/csv",
                )


with tab_save:
    st.subheader("최종 모델 저장")

    if "trained_models" not in st.session_state:
        st.info("먼저 모델을 학습하세요.")
    else:
        all_models = st.session_state["trained_models"]
        all_result_df = st.session_state["all_result_df"]

        selected_model_name = st.selectbox(
            "저장할 최종 모델 선택",
            list(all_models.keys()),
            key="save_model",
        )

        selected_payload = all_models[selected_model_name]
        st.write("선택 모델 성능")
        st.json(selected_payload["metrics"])

        if selected_payload.get("best_params"):
            st.write("최적 파라미터")
            st.json(selected_payload["best_params"])

        if st.button("선택 모델 저장", type="primary"):
            model_path, info_path, feature_path, report_path = save_model_artifacts(
                selected_model_name=selected_model_name,
                selected_payload=selected_payload,
                problem_type=st.session_state["problem_type"],
                target_column=st.session_state["target_column"],
                feature_columns=st.session_state["feature_columns"],
                metrics=selected_payload["metrics"],
                train_report_df=all_result_df,
                test_size=st.session_state["test_size"],
            )

            st.success("모델 저장 완료")
            st.code(str(model_path))
            st.code(str(info_path))
            st.code(str(feature_path))
            st.code(str(report_path))


with st.expander("requirements.txt"):
    st.code(
        """
streamlit
pandas
numpy
scikit-learn
matplotlib
joblib
        """,
        language="text",
    )

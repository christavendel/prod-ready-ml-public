from pathlib import Path
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import log_loss, accuracy_score

def train_model(train_df: pd.DataFrame) -> tuple[Pipeline, dict]:
    # Assumes `with_features` already exists (from load_data + add_features)
    df = train_df.copy()

    # Handle label name whether raw or snake_case
    target_col = "OutcomeType" if "OutcomeType" in df.columns else "outcome_type"

    # Keep only required columns and drop missing rows
    model_df = df[[target_col, "breed", "color", "days_upon_outcome"]].dropna()

    X = model_df[["breed", "color", "days_upon_outcome"]]
    y = model_df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocess = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["breed", "color"]),
            ("num", "passthrough", ["days_upon_outcome"]),
        ]
    )

    model = Pipeline(steps=[
        ("preprocess", preprocess),
        ("clf", DecisionTreeClassifier(random_state=42, max_depth=10)),
    ])

    model.fit(X_train, y_train)

    # Predicted class probabilities
    proba = model.predict_proba(X_test)
    y_pred = model.predict(X_test)
    classes = model.named_steps["clf"].classes_
    
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "log_loss": float(log_loss(y_test, proba, labels=classes)),
        "n_samples": int(len(model_df)),
        "n_features": int(X.shape[1]),
    }
    return model, metrics

def save_model(model:Pipeline, model_path: Path) -> None:
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)


def load_model(model_path: Path) -> Pipeline:
    if not model_path.is_file():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return joblib.load(model_path)


def predict_with_model(model_path: Path, input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Return actual class prediction + class probabilities.
    Expects columns: breed, color, days_upon_outcome
    """
    model = load_model(model_path)

    required_cols = ["breed", "color", "days_upon_outcome"]
    missing = [c for c in required_cols if c not in input_df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    X = input_df[required_cols].copy()
    valid_mask = ~X.isna().any(axis=1)

    classes = model.named_steps["clf"].classes_
    proba_cols = [f"proba_{c}" for c in classes]

    result = pd.DataFrame(index=input_df.index)
    result["prediction"] = pd.NA
    for col in proba_cols:
        result[col] = pd.NA

    if valid_mask.any():
        X_valid = X.loc[valid_mask]
        pred = model.predict(X_valid)
        proba = model.predict_proba(X_valid)

        result.loc[valid_mask, "prediction"] = pred
        result.loc[valid_mask, proba_cols] = proba

    return result
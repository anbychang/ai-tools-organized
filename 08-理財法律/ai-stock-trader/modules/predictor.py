"""模組 B：股價預測 — 用 Random Forest 預測未來漲跌"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def prepare_features(df, feature_cols, window=5):
    """建立滑動窗口特徵"""
    data = df[feature_cols].values
    targets = np.sign(df["Daily_Return"].shift(-1).values)  # 明天漲跌

    X, y = [], []
    for i in range(window, len(data) - 1):
        # 把前 window 天的特徵攤平
        feat = data[i - window:i].flatten()
        X.append(feat)
        y.append(targets[i])

    X = np.array(X)
    y = np.array(y)
    # 移除 nan
    mask = ~np.isnan(y) & ~np.isnan(X).any(axis=1)
    return X[mask], y[mask]


def train_predictor(df, feature_cols, window=5, **kwargs):
    """訓練預測模型"""
    print(f"[股價預測] 訓練 GBM + RandomForest（window={window}）...")

    X, y = prepare_features(df, feature_cols, window)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Model 1: Gradient Boosting
    gbm = GradientBoostingClassifier(n_estimators=100, max_depth=4, random_state=42)
    gbm.fit(X_train, y_train)
    gbm_acc = accuracy_score(y_test, gbm.predict(X_test))
    print(f"  GBM 準確率: {gbm_acc:.1%}")

    # Model 2: Random Forest
    rf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    rf.fit(X_train, y_train)
    rf_acc = accuracy_score(y_test, rf.predict(X_test))
    print(f"  Random Forest 準確率: {rf_acc:.1%}")

    # Ensemble: 投票
    gbm_pred = gbm.predict(X_test)
    rf_pred = rf.predict(X_test)
    ensemble_pred = np.sign(gbm_pred + rf_pred)
    ensemble_pred[ensemble_pred == 0] = 1  # 平手時看漲
    ensemble_acc = accuracy_score(y_test, ensemble_pred)
    print(f"[股價預測] 集成模型準確率: {ensemble_acc:.1%}")

    best_acc = max(gbm_acc, rf_acc, ensemble_acc)
    return gbm, rf, None, best_acc

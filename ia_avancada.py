import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def preparar_dados(df):
    X, y = [], []
    for i in range(5, len(df)):
        X.append(df['multiplicador'].iloc[i-5:i].values)
        y.append(1 if df.iloc[i]['multiplicador'] >= 2 else 0)
    return np.array(X), np.array(y)

def treinar_modelo():
    try:
        df = pd.read_csv("data/historico.csv")
        X, y = preparar_dados(df)

        if len(X) < 10:
            print("⚠️ Dados insuficientes para treino")
            return None

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        modelo = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        modelo.fit(X_train, y_train)

        pred = modelo.predict(X_test)
        acc = accuracy_score(y_test, pred)
        print(f"🧠 Modelo treinado | Acurácia: {acc:.2f}")

        joblib.dump(modelo, "models/modelo_atual.pkl")
        return modelo
    except Exception as e:
        print("❌ Erro ao treinar modelo:", e)
        return None
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

def prever(df):
    try:
        X = [df.iloc[-5:].values]
        modelo = joblib.load("models/modelo_atual.pkl")
        probabilidade = modelo.predict_proba(X)[0][1] * 100
        return probabilidade
    except Exception as e:
        print("❌ Erro ao prever:", e)
        return 0
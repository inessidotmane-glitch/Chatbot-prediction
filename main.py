import re
import unicodedata
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.utils.class_weight import compute_class_weight

import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')



DATA_PATH = Path("Data/dataset_universite_fr.csv")
df = pd.read_csv(DATA_PATH)

df.columns = [c.strip().lower() for c in df.columns]


def clean_text(s: str) -> str:
    s = str(s)
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)  # garder lettres/chiffres de base
    s = re.sub(r"\s+", " ", s).strip()
    return s

df["question"] = df["question"].apply(clean_text)

df = df[(df["question"].str.len() > 0) & (df["class"].notna())].copy()


#devision ensemble de données pour l'apprentissage et le test
X = df["question"].values
y = df["class"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

#ponderation de mots

stopwords_fr = stopwords.words('french')
vectorizer = TfidfVectorizer(
    stop_words=stopwords_fr,      # stopwords FR intégrés scikit-learn
    ngram_range=(1, 2),       # unigrams + bigrams
    min_df=2,                 # ignorer termes trop rares
    max_df=0.9                # ignorer termes trop fréquents
)

#preparation classes 
classes = np.unique(y_train)
class_weights = compute_class_weight(class_weight="balanced", classes=classes, y=y_train)
cw_dict = {c: w for c, w in zip(classes, class_weights)}

clf = LogisticRegression(
    max_iter=2000,
    class_weight=cw_dict,
    n_jobs=None
)

pipe = Pipeline([
    ("tfidf", vectorizer),
    ("clf", clf)
])

#entrainement 

pipe.fit(X_train, y_train)

#evaluation 
y_pred = pipe.predict(X_test)
acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, digits=3)
cm = confusion_matrix(y_test, y_pred, labels=classes)

print(f"Accuracy (test) : {acc:.4f}\n")

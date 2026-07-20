from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

class CustomIntentClassifier:
    def __init__(self, model_path="intent_model.pkl"):
        self.model_path = model_path
        self.vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
        self.clf = LogisticRegression(max_iter=200)
        self.is_trained = False
        
        if os.path.exists(model_path):
            self.load()

    def train(self, texts, labels):
        """Entrena el clasificador con listas de textos y etiquetas."""
        if len(set(labels)) < 2:
            print("⚠️ Se necesitan al menos 2 intenciones diferentes para entrenar.")
            return
        X = self.vectorizer.fit_transform(texts)
        self.clf.fit(X, labels)
        self.is_trained = True
        joblib.dump((self.vectorizer, self.clf), self.model_path)
        print(f"✅ Modelo entrenado con {len(set(labels))} intenciones, {len(texts)} ejemplos.")

    def load(self):
        self.vectorizer, self.clf = joblib.load(self.model_path)
        self.is_trained = True

    def predict(self, text):
        if not self.is_trained:
            return "unknown"
        X = self.vectorizer.transform([text])
        return self.clf.predict(X)[0]

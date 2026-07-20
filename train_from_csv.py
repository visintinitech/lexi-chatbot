import pandas as pd
from intent_classifier import CustomIntentClassifier

def train_from_csv(csv_file="training_data.csv"):
    df = pd.read_csv(csv_file)
    df = df.dropna(subset=["text", "intent"])
    df = df[df["intent"] != ""]
    
    texts = df["text"].tolist()
    labels = df["intent"].tolist()
    
    if len(set(labels)) < 2:
        print("⚠️ Necesitas al menos 2 intenciones diferentes para entrenar.")
        return
    
    clf = CustomIntentClassifier()
    clf.train(texts, labels)
    print("🎯 ¡Clasificador re-entrenado con los datos reales!")
    print(f"📊 Clases: {set(labels)}")

if __name__ == "__main__":
    train_from_csv()

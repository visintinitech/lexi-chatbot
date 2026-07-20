import spacy
from transformers import pipeline
import langdetect
import re

class LexiNLP:
    def __init__(self, use_transformers=True):
        self.spacy_models = {}
        self.default_lang = "en"
        # Cargamos modelos bajo demanda
        self.load_spacy_model("en")
        self.load_spacy_model("es")
        
        self.use_transformers = use_transformers
        if use_transformers:
            # Modelo para QA (preguntas/respuestas)
            self.qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
            # Modelo de sentimiento multilingüe
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis", 
                model="nlptown/bert-base-multilingual-uncased-sentiment"
            )
        else:
            self.sentiment_analyzer = None

        # Keywords de fallback (si no hay clasificador entrenado)
        self.intent_keywords = {
            "saludo": ["hola", "buenas", "hey", "qué tal"],
            "despedida": ["adiós", "chao", "hasta luego", "nos vemos"],
            "presentacion": ["quién eres", "qué haces", "presentate"],
            "ayuda": ["ayuda", "necesito", "cómo", "qué es"]
        }

    def load_spacy_model(self, lang):
        if lang not in self.spacy_models:
            if lang == "es":
                self.spacy_models[lang] = spacy.load("es_core_news_md")
            else:
                self.spacy_models[lang] = spacy.load("en_core_web_md")
        return self.spacy_models[lang]

    def detect_language(self, text):
        try:
            lang = langdetect.detect(text)
            if lang in ["es", "en"]:
                return lang
            return "en"
        except:
            return "en"

    def process_text(self, text):
        """Tokeniza y extrae entidades usando el modelo de idioma correcto."""
        lang = self.detect_language(text)
        nlp_model = self.load_spacy_model(lang)
        doc = nlp_model(text)
        return doc, lang

    def parse_intent(self, text, custom_classifier=None):
        """
        Parsea la intención usando el clasificador personalizado si existe,
        sino fallback a keywords.
        """
        if custom_classifier and custom_classifier.is_trained:
            intent = custom_classifier.predict(text)
            if intent != "unknown":
                return intent
        # Fallback a keywords
        text_lower = text.lower()
        for intent, keywords in self.intent_keywords.items():
            if any(k in text_lower for k in keywords):
                return intent
        return "pregunta_general"

    def extract_entities(self, text):
        doc, _ = self.process_text(text)
        entities = {ent.label_: ent.text for ent in doc.ents}
        return entities

    def get_sentiment(self, text):
        """Devuelve 'positive', 'neutral' o 'negative'."""
        if not self.sentiment_analyzer:
            return "neutral"
        try:
            result = self.sentiment_analyzer(text[:512])[0]
            score = int(result['label'][0])  # '1 star' -> 1, '5 stars' -> 5
            if score >= 4:
                return "positive"
            elif score <= 2:
                return "negative"
            else:
                return "neutral"
        except:
            return "neutral"

    def apply_tone(self, base_response, sentiment):
        """Envuelve la respuesta según el estado de ánimo detectado."""
        if sentiment == "negative":
            return f"😔 Lamento que te sientas así. {base_response} ¿Podemos ayudarte en algo más?"
        elif sentiment == "positive":
            return f"😊 ¡Qué bien me alegra! {base_response} ¿Algo más en lo que pueda asistirte?"
        else:
            return f"🤖 {base_response}"

    def answer_question(self, question, context=None):
        """
        Si usamos transformers, responde basado en un contexto.
        Si no, devuelve un mensaje genérico.
        """
        if self.use_transformers and context:
            try:
                result = self.qa_pipeline(question=question, context=context)
                return result['answer']
            except:
                pass
        # Fallback: responder con intención
        intent = self.parse_intent(question)
        return self.fallback_response(intent, question)

    def fallback_response(self, intent, text):
        responses = {
            "saludo": "¡Hola! Soy Lexi, tu asistente conversacional. ¿En qué te ayudo?",
            "despedida": "¡Hasta luego! Fue un placer hablar contigo.",
            "presentacion": "Soy Lexi, un chatbot creado con spaCy y transformers. Puedo responder preguntas simples y mantener una conversación.",
            "ayuda": "Claro, pregúntame sobre cualquier tema. Si necesito contexto, te lo pediré.",
            "pregunta_general": f"Interesante pregunta. No tengo una respuesta exacta, pero puedo buscar información. Dime más sobre '{text}'."
        }
        return responses.get(intent, "No entendí bien, ¿puedes reformularlo?")

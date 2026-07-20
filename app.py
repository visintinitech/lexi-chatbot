import requests
import feedparser
import langdetect
from deep_translator import GoogleTranslator
from nlp_engine import LexiNLP
from intent_classifier import CustomIntentClassifier
from database import Database

# Inicialización
lexi = LexiNLP(use_transformers=True)
classifier = CustomIntentClassifier()  # Carga si existe modelo entrenado
db = Database()
memory = {}  # simple memoria en RAM (por si acaso)

def handle_command(command_text, user_id):
    """Procesa comandos que empiezan con '/'."""
    parts = command_text.strip().split()
    if not parts:
        return None
    cmd = parts[0][1:].lower()

    # --- COMANDO: /weather ---
    if cmd == "weather":
        city = None
        if len(parts) > 1:
            city = " ".join(parts[1:])
        else:
            # Intentar extraer ciudad del historial reciente
            try:
                history = db.get_conversation_history(user_id, limit=5)
                user_messages = [msg[0] for msg in history if msg[0] and not msg[0].startswith("/")]
                for msg in reversed(user_messages):
                    doc, _ = lexi.process_text(msg)
                    for ent in doc.ents:
                        if ent.label_ in ["GPE", "LOC"]:
                            city = ent.text
                            break
                    if city:
                        break
            except:
                pass
        if not city:
            return "🌍 ¿Para qué ciudad quieres el clima? Ejemplo: `/weather Madrid`"
        try:
            url = f"https://wttr.in/{city}?format=%C+%t&lang=es"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                weather_info = response.text.strip()
                return f"🌤️ Clima en {city}: {weather_info}"
            else:
                return f"❌ No pude obtener el clima de {city}."
        except Exception as e:
            return f"⚠️ Error al conectar con el servicio de clima: {e}"

    # --- COMANDO: /translate ---
    elif cmd == "translate" and len(parts) >= 3:
        target_lang = parts[1]
        text_to_translate = " ".join(parts[2:])
        try:
            translated = GoogleTranslator(source='auto', target=target_lang).translate(text_to_translate)
            return f"🌍 Traducción al *{target_lang}*: {translated}"
        except Exception as e:
            return f"❌ Error en la traducción: {e}"

    # --- COMANDO: /news (con detección de idioma) ---
    elif cmd == "news":
        limit = 3
        if len(parts) > 1 and parts[1].isdigit():
            limit = min(int(parts[1]), 10)
        # Detectar idioma preferido del usuario
        preferred_lang = "en"
        try:
            history = db.get_conversation_history(user_id, limit=5)
            user_messages = [msg[0] for msg in history if msg[0] and not msg[0].startswith("/")]
            if user_messages:
                lang_counts = {"es": 0, "en": 0}
                for msg in user_messages:
                    try:
                        lang = langdetect.detect(msg)
                        if lang in lang_counts:
                            lang_counts[lang] += 1
                    except:
                        pass
                if lang_counts["es"] > lang_counts["en"]:
                    preferred_lang = "es"
                else:
                    preferred_lang = "en"
        except:
            pass

        if preferred_lang == "es":
            feed_url = "https://feeds.elpais.com/megaportada/elpais/portada.xml"
            lang_label = "español"
        else:
            feed_url = "http://feeds.bbci.co.uk/news/rss.xml"
            lang_label = "inglés"

        try:
            feed = feedparser.parse(feed_url)
            if not feed.entries:
                return "📰 No pude obtener noticias en este momento."
            headlines = []
            for entry in feed.entries[:limit]:
                title = entry.title.replace("<![CDATA[", "").replace("]]>", "").strip()
                headlines.append(f"• {title}")
            return f"📰 *Últimas noticias ({lang_label})*:\n" + "\n".join(headlines)
        except Exception as e:
            return f"⚠️ Error al obtener noticias: {e}"

    # --- COMANDO: /stats ---
    elif cmd == "stats":
        stats = db.analyze()
        if "error" in stats:
            return "📊 Aún no hay datos suficientes."
        msg = f"📊 *Estadísticas* (últimos mensajes):\n"
        msg += f"- Total: {stats['total_messages']}\n"
        msg += f"- Intenciones top: {stats['top_intents']}\n"
        msg += f"- Sentimiento: {stats['sentiment_distribution']}\n"
        msg += f"- Idiomas: {stats['language_distribution']}"
        return msg

    # --- COMANDO: /help ---
    elif cmd == "help":
        return """
📋 *Comandos disponibles:*
- `/weather [ciudad]` → Clima actual (ciudad opcional, la detecta del contexto).
- `/translate [idioma] [texto]` → Traduce (ej: `/translate en Hola`).
- `/news [número]` → Últimas noticias (detecta idioma automáticamente).
- `/stats` → Estadísticas de conversaciones.
- `/help` → Esta ayuda.
"""

    return None  # No es un comando reconocido

# ========== BUCLE PRINCIPAL ==========
if __name__ == "__main__":
    user = "usuario1"  # Para pruebas, puedes usar un ID fijo
    print("🤖 Lexi está activa. Escribe /help para ver comandos.")
    while True:
        msg = input("Tú: ")
        if msg.lower() in ["salir", "exit", "quit"]:
            print("Lexi: ¡Hasta luego! 👋")
            break

        # 1. ¿Es un comando?
        if msg.startswith("/"):
            cmd_response = handle_command(msg, user)
            if cmd_response:
                print(f"Lexi: {cmd_response}")
                # Loggear el comando
                db.log(user, msg, "command", "neutral", cmd_response, "en", command=msg)
                continue
            else:
                print("Lexi: No reconozco ese comando. Escribe /help.")
                continue

        # 2. Flujo normal
        lang = lexi.detect_language(msg)
        sentiment = lexi.get_sentiment(msg)
        intent = lexi.parse_intent(msg, custom_classifier=classifier)

        # Obtener contexto de los últimos mensajes
        history = db.get_conversation_history(user, limit=3)
        context_text = " ".join([h[0] for h in history if h[0] and not h[0].startswith("/")])

        # Generar respuesta base
        if "?" in msg or "qué" in msg or "cuál" in msg:
            base_answer = lexi.answer_question(msg, context=context_text)
        else:
            base_answer = lexi.fallback_response(intent, msg)

        # Aplicar tono según sentimiento
        final_response = lexi.apply_tone(base_answer, sentiment)

        # Guardar en BD
        db.log(user, msg, intent, sentiment, final_response, lang)

        print(f"Lexi: {final_response}")



```markdown
# 🤖 Lexi – Tu Chatbot con NLP (hecho por un dev junior, obvio)

¡Buenas! 👋 Si llegaste hasta acá es porque te copa la idea de tener tu propio asistente conversacional que entienda lo que le decís (aunque le hables en argentino). **Lexi** es un bot entrenado con **spaCy**, **Transformers**, **SQLite** y mucho mate. No es un robot cualquiera: detecta si estás contento, enojado o neutral, y te responde con el tono adecuado. Además, te da el clima, noticias de Argentina, traduce textos y hasta se puede entrenar con tus propias conversaciones para que sea más piola con el tiempo.

Si sos junior como yo y querés aprender mientras armás algo copado, este proyecto es para vos. Dale, metele.

---

## 🚀 ¿Qué hace Lexi?

- **Reconoce intenciones** (saludos, devoluciones, precios, lo que vos le enseñes).
- **Analiza sentimientos** y cambia el tono (empático, alegre o neutral).
- **Responde preguntas** con un modelo de QA (tipo los de los exámenes).
- **Comandos especiales** que funcionan en criollo:
  - `/weather [ciudad]` – Clima en tiempo real (ejemplo: `/weather Buenos Aires`).
  - `/translate [idioma] [texto]` – Traduce a lo que quieras (ej: `/translate en Hola`).
  - `/news [número]` – Últimas noticias de Argentina (Clarín/Infobae) y detecta si hablás español o inglés.
  - `/stats` – Estadísticas de las charlas (para ver qué te preguntan más).
  - `/help` – Te tira la ayuda.
- **Memoria eterna** con SQLite (no se olvida ni de lo que hablaste ayer).
- **Ciclo de mejora continua**: exportás logs, etiquetás intenciones, reentrenás y listo.

---

## 📦 Requisitos (lo que tenés que tener instalado)

- Python 3.8 o superior (si no tenés, bajalo de python.org).
- Ganas de aprender y paciencia (como cuando hacés un asado y esperás que se cocine).

Dependencias (todas en `requirements.txt`):

```txt
spacy>=3.5
transformers>=4.30
torch>=2.0
langdetect>=1.0
scikit-learn>=1.3
joblib>=1.3
requests>=2.31
deep-translator>=1.11
feedparser>=6.0
```

---

## 🛠️ Instalación (paso a paso, sin vueltas)

1. **Cloná el repo** (o descargá los archivos) y entrá a la carpeta:
   ```bash
   git clone https://github.com/tu-usuario/lexi-chatbot.git
   cd lexi-chatbot
   ```

2. **Creá un entorno virtual** (eso es buena práctica, como lavarse las manos antes de comer):
   ```bash
   python -m venv venv
   source venv/bin/activate   # en Linux/Mac
   venv\Scripts\activate      # en Windows
   ```

3. **Instalá las librerías** (paciencia, que son varias):
   ```bash
   pip install -r requirements.txt
   ```

4. **Bajá los modelos de spaCy** (para español e inglés):
   ```bash
   python -m spacy download es_core_news_md
   python -m spacy download en_core_web_md
   ```

5. **¡Listo!** Ejecutá:
   ```bash
   python app.py
   ```

---

## 🧪 Primera charla con Lexi (como cuando conocés a alguien en un bondi)

Cuando ejecutás `app.py`, te aparece un prompt. Empezá a hablarle nomás:

```text
Tú: Hola, che
Lexi: 🤖 ¡Hola! Soy Lexi, tu asistente conversacional. ¿En qué te ayudo?

Tú: ¿Cómo está el clima en Córdoba?
Lexi: 🌤️ Clima en Córdoba: Partly cloudy +28°C

Tú: /translate en Me encanta este bot
Lexi: 🌍 Traducción al en: I love this bot

Tú: /news 3
Lexi: 📰 Últimas noticias (español):
• El dólar blue subió a $1.200 hoy
• Boca ganó el clásico y es líder
• Anuncian aumento de naftas para el mes que viene
```

Para salir, escribí `salir`, `exit` o `quit` (como cuando te querés ir de una joda).

---

## 🧠 Cómo enseñarle a Lexi tus propias frases (para que sea más argentino todavía)

Lexi viene con un clasificador básico, pero lo copado es que **lo podés entrenar con tus datos**. Así va a entender mejor tus modismos.

### 📝 Paso 1: Generá logs
Usá Lexi un rato (pedile a tus amigos que también le hablen). Todo queda guardado en `lexi_chatbot.db`.

### 📤 Paso 2: Exportá a CSV
Corré:
```bash
python export_logs_to_csv.py
```
Te va a crear un archivo `training_data.csv` con dos columnas: `text` (lo que escribiste) e `intent` (la intención que Lexi adivinó).

### ✏️ Paso 3: Etiquetá a tu gusto
Abrí ese CSV con Excel, LibreOffice o el editor que te guste. Corregí la columna `intent` para que tenga el nombre que vos querés. Por ejemplo:

| text | intent |
|------|--------|
| che, quiero devolver el producto | return |
| ¿cuánto sale el envío a Rosario? | pricing |
| ¡qué copado! | happy |
| dale, gracias | thanks |

### 🏋️ Paso 4: Reentrená
Ejecutá:
```bash
python train_from_csv.py
```
Lexi va a guardar el nuevo modelo en `intent_model.pkl`. A partir de ahora, va a usar ese clasificador que vos afinaste.

**Consejo de junior**: Mientras más frases tengas (y más variadas), mejor. No tengas miedo de meter modismos argentinos, que el modelo los va a aprender.

---

## 🗂️ Estructura del proyecto (para que no te pierdas como en Once)

```
lexi_chatbot/
├── app.py                  # El corazón del asunto
├── nlp_engine.py           # Todo lo que es NLP (spaCy, transformers, sentimiento)
├── intent_classifier.py    # Clasificador personalizado con sklearn
├── database.py             # SQLite para guardar las charlas
├── export_logs_to_csv.py   # Exporta logs a CSV para etiquetar
├── train_from_csv.py       # Reentrena con tu CSV corregido
├── requirements.txt        # Las librerías necesarias
└── README.md               # Este documento
```

---

## 💡 Comandos especiales – Resumen rápido (para que no te olvides)

| Comando | Ejemplo | Qué hace |
|---------|---------|----------|
| `/weather` | `/weather La Plata` | Clima en esa ciudad (usá la que quieras). |
| `/translate` | `/translate pt Hola` | Traduce al idioma que le digas. |
| `/news` | `/news 5` | Últimas noticias de Argentina (feed de Clarín/Infobae por defecto). |
| `/stats` | `/stats` | Estadísticas de las conversaciones. |
| `/help` | `/help` | Te muestra esta tablita. |

---

## ❓ Preguntas frecuentes 

**¿Lexi entiende el lunfardo?**  
Si le enseñás con ejemplos, sí. El clasificador aprende con los datos que le des. Podés poner frases como "che, ¿cuánto sale?" o "dale, contame" y etiquetarlas bien.

**¿Puedo cambiar los feeds de noticias a otros medios?**  
Obvio. En `app.py`, en el comando `/news`, cambiá la variable `feed_url` por el RSS que quieras. Por ejemplo:
- Clarín: `https://www.clarin.com/rss/lo-ultimo/`
- Infobae: `https://www.infobae.com/arc/outboundfeeds/rss/?outputType=xml`
- La Nación: `https://www.lanacion.com.ar/arc/outboundfeeds/rss/?outputType=xml`

**¿Por qué a veces tarda en responder?**  
La primera ejecución descarga modelos pesados de Transformers. Si tenés una compu medio vieja, podés desactivarlos en `nlp_engine.py` poniendo `use_transformers=False`. Vas a perder un poco de precisión, pero va más rápido.

**¿Puedo hacer que Lexi hable con voz?**  
Por ahora no, pero podrías integrarlo con alguna API de texto a voz. Eso ya es un desafío para otro día.

---

## 🤝 ¿Querés sumar algo? (contribuciones)

Si te copa el proyecto y querés agregar comandos, mejorar el análisis de sentimiento o hacer una interfaz web, ¡adelante! Abrí un issue o un pull request. Acá todos los juniors son bienvenidos.

---

## 📜 Licencia

MIT (compartir es lo nuestro).

---

## 🧉 Último mate (de un dev junior a otro)

Armar a Lexi me llevó tiempo, pero aprendí banda: desde cómo funcionan los embeddings hasta cómo no llenar de errores la base de datos. Si te trabás en algún paso, respirá hondo, revisá los logs y preguntá. **No hay pregunta boluda, solo respuestas que no encontraste todavía.**

Ahora dale, ejecutá `python app.py` y contale a Lexi lo bien que te fue en el partido del finde. (Bueno, eso todavía no lo hace, pero quién te dice en la próxima versión).

¡Éxitos con el proyecto, loco! 🚀🤖
```

---


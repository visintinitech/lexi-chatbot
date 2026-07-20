import sqlite3
import datetime
import json
from collections import Counter

class Database:
    def __init__(self, db_path="lexi_chatbot.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_id TEXT NOT NULL,
                message TEXT NOT NULL,
                intent TEXT,
                sentiment TEXT,
                language TEXT,
                response TEXT,
                command TEXT,
                extra TEXT
            )
        ''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_user ON conversations (user_id)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON conversations (timestamp)')
        conn.commit()
        conn.close()

    def log(self, user_id, message, intent, sentiment, response, lang="en", command=None, extra=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO conversations 
            (timestamp, user_id, message, intent, sentiment, language, response, command, extra)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.datetime.now().isoformat(),
            user_id,
            message,
            intent,
            sentiment,
            lang,
            response,
            command,
            json.dumps(extra) if extra else None
        ))
        conn.commit()
        conn.close()

    def analyze(self, last_n=1000):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT intent, sentiment, language FROM conversations
            ORDER BY timestamp DESC LIMIT ?
        ''', (last_n,))
        rows = c.fetchall()
        conn.close()
        
        if not rows:
            return {"error": "No hay datos en la BD"}
        
        intents = [r[0] for r in rows if r[0]]
        sentiments = [r[1] for r in rows if r[1]]
        languages = [r[2] for r in rows if r[2]]
        
        return {
            "top_intents": Counter(intents).most_common(5),
            "sentiment_distribution": Counter(sentiments),
            "language_distribution": Counter(languages),
            "total_messages": len(rows)
        }

    def get_conversation_history(self, user_id, limit=10):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT message, response, timestamp FROM conversations
            WHERE user_id = ?
            ORDER BY timestamp DESC LIMIT ?
        ''', (user_id, limit))
        rows = c.fetchall()
        conn.close()
        return list(reversed(rows))  # orden cronológico ascendente

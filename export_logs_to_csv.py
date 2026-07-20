import csv
import sqlite3
from database import Database

def export_logs_to_sqlite_csv(output_csv="training_data.csv"):
    db = Database()
    conn = sqlite3.connect(db.db_path)
    c = conn.cursor()
    c.execute('''
        SELECT message, intent FROM conversations 
        WHERE message NOT LIKE '/%' AND message != ''
        ORDER BY timestamp DESC
    ''')
    rows = c.fetchall()
    conn.close()

    with open(output_csv, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["text", "intent"])
        for msg, intent in rows:
            writer.writerow([msg, intent if intent else "unknown"])
    
    print(f"✅ {len(rows)} mensajes exportados a {output_csv}")
    print("📝 Ahora edita ese CSV, corrige la columna 'intent' y ejecuta train_from_csv.py")

if __name__ == "__main__":
    export_logs_to_sqlite_csv()

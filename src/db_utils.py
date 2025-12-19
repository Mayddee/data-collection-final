import sqlite3
import os

def init_db():
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect('data/app.db')
    cur = conn.cursor()
    # Таблица для очищенных данных (Job 2)
    cur.execute('''CREATE TABLE IF NOT EXISTS events 
                   (timestamp DATETIME, ticker TEXT, last_price REAL, volume REAL, buy REAL, sell REAL)''')
    # Таблица для аналитики (Job 3)
    cur.execute('''CREATE TABLE IF NOT EXISTS daily_summary 
                   (date DATE, avg_last_price REAL, total_volume REAL, max_price REAL)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
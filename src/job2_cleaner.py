# from kafka import KafkaConsumer
# import json
# import sqlite3
# from datetime import datetime

# def kafka_to_sqlite():
#     consumer = KafkaConsumer(
#         'raw_tickers',
#         bootstrap_servers=['localhost:9092'],
#         auto_offset_reset='earliest',
#         consumer_timeout_ms=5000,
#         value_deserializer=lambda x: json.loads(x.decode('utf-8'))
#     )
    
#     conn = sqlite3.connect('data/app.db')
#     cur = conn.cursor()
    
#     for msg in consumer:
#         d = msg.value
#         # Конвертируем Unix timestamp в читаемую дату
#         ts = datetime.fromtimestamp(int(d['at'])).strftime('%Y-%m-%d %H:%M:%S')
        
#         cur.execute("""
#             INSERT INTO events (timestamp, ticker, last_price, volume, buy, sell) 
#             VALUES (?, ?, ?, ?, ?, ?)
#         """, (ts, d['ticker'], float(d['last']), float(d['volume']), float(d['buy']), float(d['sell'])))
    
#     conn.commit()
#     conn.close()

from kafka import KafkaConsumer
import json
import sqlite3
import os

def kafka_to_sqlite():
    db_path = '/Users/amangeldimadina/Desktop/data-gathering/data-final/data/app.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Создаем таблицу точно как на твоем скриншоте
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            timestamp INTEGER,
            ticker TEXT,
            last_price REAL,
            volume REAL,
            buy REAL,
            sell REAL
        )
    ''')
    conn.commit()

    consumer = KafkaConsumer(
        'raw_events',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='group_v2', # Поменял ID группы, чтобы он заново прочитал Кафку
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        consumer_timeout_ms=10000 # Ждем 10 секунд
    )

    print("Starting cleaning process...")
    count = 0
    for message in consumer:
        data = message.value
        try:
            # Сопоставляем ключи из API WazirX с твоими колонками
            row = (
                int(data.get('at', 0)),          # timestamp
                data.get('symbol'),              # ticker
                float(data.get('lastPrice', 0)), # last_price
                float(data.get('volume', 0)),    # volume
                float(data.get('bidPrice', 0)),  # buy
                float(data.get('askPrice', 0))   # sell
            )
            cursor.execute('INSERT INTO events VALUES (?,?,?,?,?,?)', row)
            count += 1
        except Exception as e:
            print(f"Skipping record due to error: {e}")

    conn.commit()
    conn.close()
    consumer.close()
    print(f"Successfully inserted {count} records.")
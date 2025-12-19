# import requests
# import json
# from kafka import KafkaProducer
# from datetime import datetime
# import time

# def stream_to_kafka():
#     # Настройка продюсера
#     producer = KafkaProducer(
#         bootstrap_servers=['localhost:9092'],
#         value_serializer=lambda v: json.dumps(v).encode('utf-8'),
#         # Добавим таймаут, чтобы не зависать при подключении
#         request_timeout_ms=5000 
#     )
    
#     url = "https://api.wazirx.com/api/v2/tickers"
    
#     try:
#         response = requests.get(url, timeout=10)
#         data = response.json()
        
#         # Берем BTC/INR (в ключе "btcinr")
#         ticker_key = 'btcinr'
#         if ticker_key in data:
#             item = data[ticker_key]
#             payload = {
#                 "ticker": item['name'],       # "BTC/INR"
#                 "last": item['last'],         # Цена последней сделки
#                 "volume": item['volume'],     # Объем
#                 "buy": item['buy'],
#                 "sell": item['sell'],
#                 "at": item['at']              # Timestamp
#             }
            
#             producer.send('raw_tickers', payload)
#             print(f"Успешно отправлено в Kafka: {payload['ticker']} - {payload['last']}")
#         else:
#             print(f"Ключ {ticker_key} не найден в ответе API")
            
#     except Exception as e:
#         print(f"Ошибка при работе с API или Kafka: {e}")
#     finally:
#         producer.flush()

# if __name__ == "__main__":
#     stream_to_kafka()

# import requests
# import json
# from kafka import KafkaProducer
# import time

# def stream_to_kafka():
#     producer = KafkaProducer(
#         bootstrap_servers=['data-final-kafka-1:9092'],
#         request_timeout_ms=5000,
#         value_serializer=lambda v: json.dumps(v).encode('utf-8')
#     )
    
#     topic = 'raw_events'
#     url = "https://api.wazirx.com/sapi/v1/tickers/24hr"
    
#     try:
#         response = requests.get(url, timeout=10)
#         if response.status_code == 200:
#             data = response.json()
#             # Если данных много, отправляем только часть или все сразу
#             for item in data[:50]: # берем первые 50 записей для теста
#                 producer.send(topic, item)
            
#             producer.flush()
#             print(f"Successfully sent {len(data[:50])} records to Kafka.")
#         else:
#             print(f"API Error: {response.status_code}")
#     except Exception as e:
#         print(f"Error in producer: {e}")
#     finally:
#         producer.close()

import requests
import json
from kafka import KafkaProducer
import time

# Настройки
TOPIC = 'raw_events'
# Используем localhost, так как ты запускаешь скрипт из терминала Мака
BOOTSTRAP_SERVERS = ['localhost:9092'] 
URL = "https://api.wazirx.com/sapi/v1/tickers/24hr"

def stream_to_kafka():
    print(f"Connecting to Kafka at {BOOTSTRAP_SERVERS}...")
    try:
        producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            request_timeout_ms=5000,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        print(f"Fetching data from {URL}...")
        response = requests.get(url=URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Отправляем записи в Кафку
            for item in data[:50]: 
                producer.send(TOPIC, item)
            
            producer.flush()
            print(f"УСПЕХ: Отправлено {len(data[:50])} записей в топик {TOPIC}")
        else:
            print(f"Ошибка API: {response.status_code}")
            
        producer.close()
        
    except Exception as e:
        print(f"ОШИБКА в работе продьюсера: {e}")

if __name__ == "__main__":
    print("Запуск бесконечного цикла отправки данных...")
    while True:
        stream_to_kafka()
        print("Ждем 60 секунд до следующей итерации...")
        time.sleep(60)
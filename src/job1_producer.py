# import requests
# import json
# from kafka import KafkaProducer
# import time

# TOPIC = 'raw_events'
# BOOTSTRAP_SERVERS = ['localhost:9092'] 
# URL = "https://api.wazirx.com/sapi/v1/tickers/24hr"

# def stream_to_kafka():
#     print(f"Connecting to Kafka at {BOOTSTRAP_SERVERS}...")
#     try:
#         producer = KafkaProducer(
#             # bootstrap_servers=BOOTSTRAP_SERVERS,
#             # request_timeout_ms=5000,
#             # value_serializer=lambda v: json.dumps(v).encode('utf-8')
#             bootstrap_servers=['localhost:9092'],
#             value_serializer=lambda v: json.dumps(v).encode('utf-8'),
#             acks=1,        
#             retries=0,    
#             request_timeout_ms=5000
#         )
        
#         print(f"Fetching data from {URL}...")
#         response = requests.get(url=URL, timeout=10)
        
#         if response.status_code == 200:
#             data = response.json()
#             for item in data[:50]: 
#                 producer.send(TOPIC, item)
            
#             producer.flush()
#             print(f"Succes: Sent {len(data[:50])} records to topic {TOPIC}")
#         else:
#             print(f"API ERROR: {response.status_code}")
            
#         producer.close()
        
#     except Exception as e:
#         print(f"Error in produce work: : {e}")

# if __name__ == "__main__":
#     stream_to_kafka()

import requests
import json
from kafka import KafkaProducer

# Настройки
TOPIC = 'raw_events'
BOOTSTRAP_SERVERS = ['localhost:9092'] 
URL = "https://api.wazirx.com/sapi/v1/tickers/24hr"

def stream_to_kafka():
    print(f"Connecting to Kafka at {BOOTSTRAP_SERVERS}...")
    producer = None
    try:
        producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks=1,        
            retries=3,    
            request_timeout_ms=5000
        )
        
        print(f"Fetching data from {URL}...")
        response = requests.get(url=URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            records = data[:50]
            for item in records: 
                producer.send(TOPIC, item)
            
            producer.flush()
            print(f"SUCCESS: Sent {len(records)} records to topic {TOPIC}")
        else:
            print(f"API ERROR: {response.status_code}")
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        raise e
    finally:
        if producer:
            producer.close()
            print("Connection closed.")

if __name__ == "__main__":
    stream_to_kafka()
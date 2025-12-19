
🌟 Project Overview

This project demonstrates a **complete streaming + batch data pipeline** using **Python, Apache Airflow, Kafka, and SQLite**.  
It covers the **full lifecycle of real-time data**: ingestion, cleaning, storage, and analytical aggregation.

 Airflow DAGs

1. Continuous ingestion: WazirX API → Kafka  
2. Hourly batch processing: Kafka → SQLite (events table)  
3. Daily analytics: SQLite → aggregated summary (daily_summary table)  

---

 🔗 API Selection

WazirX Cryptocurrency Tickers API
Endpoint: [https://api.wazirx.com/api/v2/tickers](https://api.wazirx.com/api/v2/tickers)

Why WazirX?

- Frequently updated (prices change multiple times per hour)  
- Stable, documented, and widely used  
- Structured JSON output  
- Returns real trading data: prices, volumes, timestamps  

---

 🏗️ System Architecture

Lambda-style pipeline:

```

WazirX API → Airflow DAG 1 → Kafka (raw_events) → Airflow DAG 2 → SQLite (events) → Airflow DAG 3 → SQLite (daily_summary)



## ⚡ How to Run the Project

### 1️⃣ Create & Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
````

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Start Kafka & Zookeeper

```bash
docker-compose up -d
```

* Bootstrap server: `localhost:9092`
* Kafka topic: `raw_events`

### 4️⃣ Run Scripts (Optional for Testing)

```bash
python src/job1_producer.py
python src/job2_cleaner.py
python src/job3_analytics.py
```

### 5️⃣ Run Airflow

#### Standalone Mode

```bash
export AIRFLOW_HOME=$(pwd)/airflow
airflow standalone
```

Access Web UI: [http://localhost:8080](http://localhost:8080)

#### Separate Components

* **Scheduler:**

```bash
export AIRFLOW_HOME=$(pwd)/airflow
airflow scheduler
```

* **Webserver:**

```bash
export AIRFLOW_HOME=$(pwd)/airflow
airflow webserver -p 8080
```

---

## 📊 SQLite Schema

**events Table**

| Column       | Type      | Description         |
| ------------ | --------- | ------------------- |
| id           | INTEGER   | Primary key         |
| symbol       | TEXT      | Trading pair symbol |
| last_price   | REAL      | Last traded price   |
| open_price   | REAL      | Opening price       |
| high_price   | REAL      | Highest price       |
| low_price    | REAL      | Lowest price        |
| volume       | REAL      | Trading volume      |
| quote_volume | REAL      | Quote asset volume  |
| event_time   | TIMESTAMP | Event timestamp     |

**daily_summary Table**

| Column       | Type    | Description         |
| ------------ | ------- | ------------------- |
| summary_date | DATE    | Aggregation date    |
| symbol       | TEXT    | Trading pair symbol |
| avg_price    | REAL    | Average daily price |
| min_price    | REAL    | Minimum daily price |
| max_price    | REAL    | Maximum daily price |
| total_volume | REAL    | Total daily volume  |
| record_count | INTEGER | Number of records   |



## 🛠️ Technologies Used

* **Python**
* **Apache Kafka**
* **Apache Airflow**
* **SQLite**
* **Pandas**
* **WazirX Cryptocurrency Tickers API** – [https://api.wazirx.com/api/v2/tickers](https://api.wazirx.com/api/v2/tickers)




## Notes

* Ensure Kafka is running before starting Airflow DAGs.
* Optional: test scripts individually before running scheduled DAGs.
* All times are in UTC by default.



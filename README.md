Project Overview 
The goal of this project is to design and implement a complete streaming + batch data 
pipeline using Apache Airflow, Apache Kafka, and SQLite. The pipeline demonstrates the 
full lifecycle of frequently updated real-world data: ingestion, cleaning, storage, and 
analytical aggregation. 
The system consists of three Airflow DAGs: 
1. Continuous ingestion of live cryptocurrency data from an external API into Kafka 
2. Hourly batch processing to clean and store data in SQLite 
3. Daily analytics job to compute aggregated metrics and store them in a summary table 
3. API Selection and Justification 
Chosen API 
WazirX Cryptocurrency Tickers API 
Endpoint: https://api.wazirx.com/api/v2/tickers 
Justification 
The WazirX API was selected because it fully satisfies all project requirements: 
 Frequently updated: Cryptocurrency prices change continuously and update multiple 
times per hour 
 Stable and documented: Publicly available and widely used exchange API 
 Structured JSON format: Returns well-structured JSON objects 
Each API call returns the latest ticker information for multiple trading pairs, including price, 
volume, and timestamps, making it ideal for streaming and analytics use cases. 
4. System Architecture Overview 
The architecture follows a Lambda-style pipeline combining pseudo-streaming and batch 
processing.  
Data Flow 
API → Airflow DAG 1 → Kafka (raw_events) → Airflow DAG 2 → SQLite (events) → 
Airflow DAG 3 → SQLite (daily_summary) 

## How to Run the Project

### 1. Create and Activate Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```



### 2. Install Dependencies

```bash
pip install -r requirements.txt
```



### 3. Start Kafka (Local Setup)

Kafka and Zookeeper can be started using **Docker Compose**:

```bash
docker-compose up -d
```

Check that Kafka is running:

* **Bootstrap server**: `localhost:9092`
* **Kafka topic**: `raw_events`

Ensure the Docker containers for Kafka and Zookeeper are up and healthy before starting the pipeline.



### 4. Run Scripts Manually (Optional – for Testing)

Each job can be tested independently without Airflow:

```bash
python src/job1_producer.py     # WazirX API → Kafka
python src/job2_cleaner.py      # Kafka → SQLite (events)
python src/job3_analytics.py    # SQLite → daily_summary
```

This step is optional and mainly used for debugging and validation.



### 5. Run Airflow

Set Airflow home directory:

```bash
export AIRFLOW_HOME=$(pwd)/airflow
```

#### Option A: Run Airflow in Standalone Mode

```bash
airflow standalone
```

Access Airflow Web UI at:
 [http://localhost:8080](http://localhost:8080)



#### Option B: Run Airflow Components Separately

##### Start Scheduler

```bash
export AIRFLOW_HOME=$(pwd)/airflow
airflow scheduler
```

##### Start Web Interface

```bash
export AIRFLOW_HOME=$(pwd)/airflow
airflow webserver -p 8080
```

Open in browser:
 [http://localhost:8080](http://localhost:8080)

From the web interface, all three DAGs can be triggered and monitored.



## Technologies Used

* **Python**
* **Apache Kafka**
* **Apache Airflow**
* **SQLite**
* **Pandas**
* **WazirX Cryptocurrency Tickers API** – `https://api.wazirx.com/api/v2/tickers`



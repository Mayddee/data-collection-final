import sqlite3
import pandas as pd
from datetime import datetime

def run_analytics_and_report():
    db_path = '/Users/amangeldimadina/Desktop/data-gathering/data-final/data/app.db'
    conn = sqlite3.connect(db_path)
    
    try:
        # Читаем данные из исправленной таблицы
        df = pd.read_sql_query("SELECT * FROM events", conn)
        
        if df.empty:
            print("Events table is empty. Nothing to analyze.")
            return

        # Делаем расчеты по колонкам ticker и last_price
        summary = df.groupby('ticker').agg({
            'last_price': ['mean', 'max'],
            'volume': 'sum'
        }).reset_index()
        
        summary.columns = ['date', 'avg_last_price', 'max_price', 'total_volume']
        summary['date'] = str(datetime.now().date())

        # Сохраняем 
        summary.to_sql('daily_summary', conn, if_exists='replace', index=False)
        print("Analytics successfully saved to daily_summary.")
        
    finally:
        conn.close()


if __name__ == "__main__":
    run_analytics_and_report()
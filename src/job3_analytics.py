# import sqlite3
# import pandas as pd
# from datetime import datetime
# from fpdf import FPDF

# def run_analytics_and_report():
#     conn = sqlite3.connect('data/app.db')
#     df = pd.read_sql("SELECT * FROM events", conn)
    
#     if not df.empty:
#         # 1. Расчет метрик
#         avg_p = df['last_price'].mean()
#         total_v = df['volume'].sum()
#         max_p = df['last_price'].max()
#         today = str(datetime.now().date())
        
#         cur = conn.cursor()
#         cur.execute("INSERT INTO daily_summary VALUES (?,?,?,?)", (today, avg_p, total_v, max_p))
#         conn.commit()

#         # 2. Генерация PDF
#         pdf = FPDF()
#         pdf.add_page()
#         pdf.set_font("Arial", 'B', 16)
#         pdf.cell(200, 10, txt="Daily Crypto Report (WazirX)", ln=True, align='C')
#         pdf.set_font("Arial", size=12)
#         pdf.ln(10)
#         pdf.cell(200, 10, txt=f"Date: {today}", ln=True)
#         pdf.cell(200, 10, txt=f"Average Price BTC: {avg_p:.2f} INR", ln=True)
#         pdf.cell(200, 10, txt=f"Total Volume: {total_v:.4f}", ln=True)
#         pdf.cell(200, 10, txt=f"Max Price: {max_p:.2f} INR", ln=True)
#         pdf.output("report/report.pdf")
        
#     conn.close()
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
        
        # Переименовываем колонки точно под твой скриншот таблицы daily_summary
        summary.columns = ['date', 'avg_last_price', 'max_price', 'total_volume']
        # Вместо даты пока поставим просто имя тикера или текущую дату
        summary['date'] = str(datetime.now().date())

        # Сохраняем (if_exists='replace' обновит таблицу полностью)
        summary.to_sql('daily_summary', conn, if_exists='replace', index=False)
        print("Analytics successfully saved to daily_summary.")
        
    finally:
        conn.close()
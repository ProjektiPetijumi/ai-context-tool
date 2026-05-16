import mysql.connector
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
model_ai = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# 1. Savienojums ar MySQL
conn = mysql.connector.connect(
    host="87.110.123.151",
    port=3306,
    user="fita",
    password="2026-04-28"
)
cursor = conn.cursor()

# 2. Izgūst datubāzu sarakstu
cursor.execute("SHOW DATABASES;")
databases = [row[0] for row in cursor.fetchall()
             if row[0] not in ('information_schema', 'mysql', 
                               'performance_schema', 'sys')]
print(f"Atrastās datubāzes: {databases}")

# 3. Izgūst tabulu un kolonnu info
konteksts = ""
for db in databases:
    cursor.execute(f"USE `{db}`;")
    cursor.execute("SHOW TABLES;")
    tables = [row[0] for row in cursor.fetchall()]
    konteksts += f"\nDatubāze: {db}\n"
    for table in tables:
        cursor.execute(f"DESCRIBE `{table}`;")
        columns = cursor.fetchall()
        konteksts += f"  Tabula: {table}\n"
        for col in columns:
            konteksts += f"    - {col[0]} | tips: {col[1]} | null: {col[2]} | key: {col[3]}\n"

print("\n=== SERVERA KONTEKSTS ===")
print(konteksts)

# 4. Gemini ģenerē SQL vaicājumus
prompt = f"""
Šis ir MySQL servera struktūras apraksts:
{konteksts}

Izvēlies 3 svarīgākos agregētos rādītājus, ko var aprēķināt no šiem datiem.
Katram rādītājam uzraksti:
1. Nosaukumu
2. SQL vaicājumu
3. Kāpēc tas ir svarīgi
"""

response = model_ai.chat.completions.create(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    messages=[{"role": "user", "content": prompt}]
)
print("\n=== GEMINI IETEIKTIE RĀDĪTĀJI ===")
print(response.choices[0].message.content)

# 5. Izpilda AI ieteiktos SQL vaicājumus un apraksta rezultātus
sql_vaicajumi = [
    "SELECT SUM(amount) AS total_revenue FROM payments;",
    "SELECT AVG(amount) AS average_payment FROM payments;",
    """SELECT o.parent_vertical, SUM(p.amount) AS total_revenue
       FROM payments p
       JOIN mandates m ON p.mandate_id = m.id
       JOIN organisations o ON m.organisation_id = o.id
       GROUP BY o.parent_vertical
       ORDER BY total_revenue DESC;"""
]

print("\n=== AGREGĒTO DATU REZULTĀTI ===")
rezultati = ""
for sql in sql_vaicajumi:
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        rezultati += f"\nSQL: {sql}\nRezultāts: {rows}\nKolonnas: {cols}\n"
        print(f"\nSQL: {sql}")
        print(f"Rezultāts: {rows}")
    except Exception as e:
        print(f"Kļūda: {e}")

# 6. AI apraksta rezultātus
apraksts_prompt = f"""
Šie ir agregēto SQL vaicājumu rezultāti:
{rezultati}

Apraksti šos rezultātus vienkāršā latviešu valodā, skaidrojot ko tie nozīmē biznesam.
"""
apraksts = model_ai.chat.completions.create(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    messages=[{"role": "user", "content": apraksts_prompt}]
)
print("\n=== AI REZULTĀTU APRAKSTS ===")
print(apraksts.choices[0].message.content)

cursor.close()
conn.close()
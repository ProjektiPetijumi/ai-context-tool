import mysql.connector
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model_ai = genai.GenerativeModel("gemini-pro")

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

response = model_ai.generate_content(prompt)
print("\n=== GEMINI IETEIKTIE RĀDĪTĀJI ===")
print(response.text)

cursor.close()
conn.close()
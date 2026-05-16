import mysql.connector
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
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

# 4. AI ģenerē SQL vaicājumus
prompt = f"""
Šis ir MySQL servera struktūras apraksts:
{konteksts}
Izvēlies 3 svarīgākos agregētos rādītājus, ko var aprēķināt no šiem datiem.
Katram rādītājam uzraksti:
1. Nosaukumu
2. SQL vaicājumu
3. Kāpēc tas ir svarīgi
"""

response = client.chat.completions.create(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    messages=[{"role": "user", "content": prompt}]
)

print("\n=== AI IETEIKTIE RĀDĪTĀJI ===")
print(response.choices[0].message.content)

cursor.close()
conn.close()
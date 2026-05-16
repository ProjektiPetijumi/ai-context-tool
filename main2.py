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

# 2. Izgūst servera kontekstu
konteksts = ""
cursor.execute("SHOW DATABASES;")
databases = [row[0] for row in cursor.fetchall()
             if row[0] not in ('information_schema', 'mysql', 
                               'performance_schema', 'sys')]
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

print("Konteksts iegūts!")

# 3. AI izveido analīzes plānu
plans_prompt = f"""
Šis ir MySQL servera struktūras apraksts:
{konteksts}

Izveido analīzes plānu ar 5 datu vizualizācijām biznesam.
Katram plāna punktam norādi:
NOSAUKUMS: [vizualizācijas nosaukums]
TIPS: [bar/line/pie]
APRAKSTS: [ko vizualizēt]
---
"""

response = client.chat.completions.create(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    messages=[{"role": "user", "content": plans_prompt}]
)

plans = response.choices[0].message.content
print("\n=== ANALĪZES PLĀNS ===")
print(plans)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def grafiks_uz_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img

html_saturs = "<html><head><meta charset='utf-8'><title>Datu analīze</title></head><body>"
html_saturs += f"<h1>Direct Payments Analīze</h1>"

# Vizualizācija 1 - Mēneša maksājumu tendence
cursor.execute("""
    SELECT DATE_FORMAT(charge_date, '%Y-%m') as menesis, SUM(amount) as kopsumma
    FROM payments WHERE charge_date IS NOT NULL
    GROUP BY menesis ORDER BY menesis
""")
dati1 = cursor.fetchall()
x1 = [r[0] for r in dati1]
y1 = [r[1] for r in dati1]
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(x1, y1, marker='o', color='blue')
ax.set_title('Mēneša maksājumu tendence')
ax.set_xlabel('Mēnesis')
ax.set_ylabel('Summa')
plt.xticks(rotation=45)
img1 = grafiks_uz_base64(fig)
html_saturs += f"<h2>1. Mēneša maksājumu tendence</h2><img src='data:image/png;base64,{img1}'/>"

# Vizualizācija 2 - Mandātu tipu skaits
cursor.execute("SELECT scheme, COUNT(*) as skaits FROM mandates GROUP BY scheme ORDER BY skaits DESC")
dati2 = cursor.fetchall()
x2 = [r[0] for r in dati2]
y2 = [r[1] for r in dati2]
fig, ax = plt.subplots(figsize=(8,5))
ax.bar(x2, y2, color='green')
ax.set_title('Mandātu tipu skaits')
ax.set_xlabel('Schema')
ax.set_ylabel('Skaits')
img2 = grafiks_uz_base64(fig)
html_saturs += f"<h2>2. Mandātu tipu skaits</h2><img src='data:image/png;base64,{img2}'/>"

# Vizualizācija 3 - Valūtu struktūra
cursor.execute("SELECT currency, SUM(amount) as kopsumma FROM payments GROUP BY currency")
dati3 = cursor.fetchall()
x3 = [r[0] for r in dati3]
y3 = [r[1] for r in dati3]
fig, ax = plt.subplots(figsize=(7,7))
ax.pie(y3, labels=x3, autopct='%1.1f%%')
ax.set_title('Maksājumu valūtu struktūra')
img3 = grafiks_uz_base64(fig)
html_saturs += f"<h2>3. Valūtu struktūra</h2><img src='data:image/png;base64,{img3}'/>"

# Vizualizācija 4 - Organizāciju veidi
cursor.execute("SELECT parent_vertical, COUNT(*) as skaits FROM organisations GROUP BY parent_vertical ORDER BY skaits DESC")
dati4 = cursor.fetchall()
x4 = [r[0] for r in dati4]
y4 = [r[1] for r in dati4]
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(x4, y4, color='orange')
ax.set_title('Organizāciju veidi')
plt.xticks(rotation=45, ha='right')
img4 = grafiks_uz_base64(fig)
html_saturs += f"<h2>4. Organizāciju veidi</h2><img src='data:image/png;base64,{img4}'/>"

# Vizualizācija 5 - Vidējais maksājums pa mēnešiem
cursor.execute("""
    SELECT DATE_FORMAT(charge_date, '%Y-%m') as menesis, AVG(amount) as videjais
    FROM payments WHERE charge_date IS NOT NULL
    GROUP BY menesis ORDER BY menesis
""")
dati5 = cursor.fetchall()
x5 = [r[0] for r in dati5]
y5 = [r[1] for r in dati5]
fig, ax = plt.subplots(figsize=(10,5))
ax.scatter(range(len(x5)), y5, color='red')
ax.set_title('Vidējais maksājums pa mēnešiem')
ax.set_xlabel('Mēnesis')
ax.set_ylabel('Vidējais (€)')
plt.xticks(range(len(x5)), x5, rotation=45)
img5 = grafiks_uz_base64(fig)
html_saturs += f"<h2>5. Vidējais maksājums pa mēnešiem</h2><img src='data:image/png;base64,{img5}'/>"

html_saturs += "</body></html>"

with open('atskaite.html', 'w', encoding='utf-8') as f:
    f.write(html_saturs)

print("\nHTML atskaite saglabāta: atskaite.html")
cursor.close()
conn.close()
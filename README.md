# AI Context Tool

Projekts izstrādāts kā daļa no kursa par AI rīku izstrādi ar MySQL un Power BI.

## Uzdevums 1B — Datubāzes konteksta rīks
- `main.py` — savienojas ar MySQL, izgūst struktūru, LLM iesaka rādītājus un izpilda SQL

## Uzdevums 2B — HTML atskaite
- `main2.py` — ģenerē HTML atskaiti ar 5 vizualizācijām un AI aprakstiem
- `atskaite.html` — gatavā atskaite ar grafikiem un biznesa analīzi

## Uzdevums 1A/2A — Power BI
- `ai_context_tool.pbix` — Power BI dashboard ar 2 lapām:
  - Lapa 1: KPI kartītes, stabiņu grafiki, gredzena diagramma, tabula
  - Lapa 2: 4 Python vizuāļi (histogramma, boxplot, scatter, stabiņu grafiks)
- `Savienojumu kpsavilkums.jpg` — LLM ieteiktie savienojumi starp tabulām
- `BIZNESA ANALĪZES PLĀNS.jpg` — LLM izstrādāts analīzes plāns

## Tehnoloģijas
- Python, MySQL, Gemini API, matplotlib, pandas, BeautifulSoup
- Power BI Desktop (ar Python vizuāļiem)

## Uzdevums 03 — Atskaišu izveide
- `ai_context_tool.pbix` — uzlabota Power BI atskaite ar:
  - Filtri: source (checkbox) un charge_date (datuma diapazons)
  - Tumšā tēma un latviešu fonti
  - Paskaidrojumi pie katra vizuāļa
  - Report Page Tooltip
  - Interaktīvas pogas ar grāmatzīmēm (Visi kanāli / API skats)

# Direct Payments Analīze — Power BI Atskaite

## Apraksts
Power BI atskaite par maksājumu datiem no direct_payments datubāzes.

## Saturs
- **Lapa 1** — Galvenais dashboard ar filtriem
- **Lapa 2** — Detalizēta statistika (valūtas, sadalījums)
- **Tooltip** — Rīku padoma lapa

## Funkcionalitāte
- Filtri: `source` (checkbox) un `charge_date` (datuma diapazons)
- Interaktīvas pogas: "Visi kanāli" / "API skats"
- Tumšā tēma ar latviešu fontiem
- Paskaidrojumi pie katra vizuāļa
- Report Page Tooltip

## Dati
MySQL datubāze `direct_payments` ar tabulām:
- `payments` — maksājumu dati
- `mandates` — mandāti
- `organisations` — organizācijas

TMDB Filmu Analīze — Power BI Dashboard
Projekta apraksts
Power BI atskaite, kas analizē TMDB (The Movie Database) datus, izmantojot MySQL servera savienojumu. Atskaite vizualizē filmas pēc žanriem, popularitātes un valstīm.
Datu avots

Serveris: 87.110.123.151
Datubāze: tmdb
Galvenās tabulas: movies, genres, movie_genres, production_countries

Atskaites saturs
Vizualizācijas

📊 Filmas pa žanriem — stabiņu grafiks ar populārāko žanru skaitu
🏆 TOP 10 populārākās filmas — horizontāls stabiņu grafiks pēc popularity
🌍 Filmas pa valstīm — gredzena grafiks ar ražotājvalstu sadalījumu
🔢 Kopējais filmas skaits — KPI kartīte (10 000 filmas)

ZPD Vērtēšanas rīks ar AI analīzi
Projekta apraksts
Streamlit web aplikācija skolotājiem ZPD (Zinātniski Pētnieciskais Darbs) vērtēšanai. Aplikācija ļauj ievadīt skolēnu vērtējumus, skatīt statistiku un automātiski analizēt rezultātus ar AI (Claude API).
Funkcionalitāte
📝 Ievadīt vērtējumu

Skolotājs ievada skolēna vārdu, uzvārdu, klasi un mācību gadu
Punkti tiek ievadīti 10 kritērijos (kopā 100 punkti)
Automātiski aprēķina balli un nosaka vai skolēns kvalificējas uz novadu

📊 Skatīt datus

Tabula ar visiem ievadītajiem vērtējumiem
Filtri pēc gada, klases un minimālās balles

📈 Statistika un TOP 10

Vispārējā statistika (skolēnu skaits, vidējā balle, max/min punkti)
TOP 10 skolēni uz novada konkursu (balle ≥ 8, 2025/2026)
Grafiki: balles sadalījums un vidējā balle pa gadiem
Statistika pa klasēm
🤖 AI analīze — automātisks komentārs par klases rezultātiem

Vērtēšanas kritēriji
KritērijsMaks. punktiKoncepcija16Literatūra10Metodes10Rezultāti20Secinājumi6Ētika2Noformējums12Pienesums4Aizstāvēšana10MI izmantošana10Kopā100
Instalācija un palaišana
bashpip install streamlit pandas matplotlib requests
python -m streamlit run zpd_app.py
Aplikācija pieejama: http://localhost:8501
Faili

zpd_app.py — galvenais Streamlit aplikācijas fails
zpd_rezultati.csv — saglabātie skolēnu vērtējumi (tiek izveidots automātiski)

Tehnoloģijas

Python
Streamlit
Pandas
Matplotlib
Claude API (AI analīzei)

Dati
Projekts izmanto izfantazētus skolēnu datus (237 skolēni, 3 mācību gadi, 11 klases) — reālie dati netiek publicēti.
Funkcionalitāte

🔍 Filtri — žanrs un release_date
💡 Tooltip lapa — detalizēta info uzsverot peli virs grafikiem
🔘 Grāmatzīmju pogas — skatu pārslēgšana

Faili

tmdb_analysis.pbix — Power BI atskaites fails

Tehnoloģijas

Power BI Desktop
MySQL savienojums (DirectQuery / Import)

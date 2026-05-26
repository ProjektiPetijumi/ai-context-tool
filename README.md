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

Funkcionalitāte

🔍 Filtri — žanrs un release_date
💡 Tooltip lapa — detalizēta info uzsverot peli virs grafikiem
🔘 Grāmatzīmju pogas — skatu pārslēgšana

Faili

tmdb_analysis.pbix — Power BI atskaites fails

Tehnoloģijas

Power BI Desktop
MySQL savienojums (DirectQuery / Import)

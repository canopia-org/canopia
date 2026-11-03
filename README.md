# Canopia

Gemello digitale della copertura arborea di Trento: benefici ecosistemici, irrigazione mirata e percorsi all'ombra.

Progetto del corso di Ingegneria del Software, A.A. 2026-27, Prof. Paolo Giorgini (Università di Trento), per il Comune di Trento.

## Struttura del repository

```
canopia/
├── docs/                    # Deliverable del corso
│   ├── D1-Requirements.md   # Requirements Engineering (+ .pdf)
│   ├── D2-Specification.md  # AI-Ready Software Specification (+ .pdf)
│   ├── D3-TechnicalPlan.md  # Technical Plan, Tasks, Implementation & Testing (+ .pdf)
│   └── diagrammi/           # Sorgenti PlantUML, SVG e mockup, prefissati per deliverable (d1-, d2-, d3-)
├── api/
│   └── openapi.yaml         # Specifica OpenAPI 3.0 dell'API REST (D3, sez. 3)
├── data/                    # Dati di lavoro, non versionati (si generano con gli script)
├── scripts/
│   ├── build-pdf.py         # Genera il PDF di un deliverable
│   └── scarica_alberi.py    # Scarica il censimento alberi in data/
├── backend/                 # API Node.js/Express (src/, test/)
├── frontend/                # SPA Vue 3 + Vite (src/, test/)
├── .github/workflows/       # CI e deploy del frontend su GitHub Pages
└── render.yaml              # Deploy di API e worker su render.com
```

## Sviluppo

Requisiti: Node.js 24 (vedi `.nvmrc`), Docker per MongoDB locale (`docker compose up -d`) oppure una stringa di connessione MongoDB Atlas.

```bash
npm install
```

```bash
cp .env.example backend/.env
```

```bash
npm run dev -w backend
```

```bash
npm run dev -w frontend
```

L'API risponde su `http://localhost:3000/api/v1/health`, il frontend su `http://localhost:5173`.

Frontend con API simulate (MSW), senza backend:

```bash
npm run dev:mock -w frontend
```

Prima di ogni commit husky esegue lint-staged (ESLint e Prettier sui file modificati). Controlli eseguiti anche dalla CI a ogni Pull Request:

```bash
npm run lint
```

```bash
npm test
```

```bash
npm run openapi:lint
```

```bash
npm run openapi:routes
```

## Deploy

- **Frontend:** a ogni push su `main` il workflow `pages.yml` pubblica `frontend/` su GitHub Pages. Va attivato una volta in Settings → Pages → Source: GitHub Actions, e va impostata la variabile di repository `VITE_API_URL`.
- **API:** collegare il repository a render.com come Blueprint (`render.yaml`) e impostare `MONGODB_URI` dalla dashboard.

## Documenti

Generare il PDF di un deliverable (richiede Node e Google Chrome):

```bash
python3 scripts/build-pdf.py D1-Requirements
```

Rigenerare un diagramma (richiede PlantUML):

```bash
plantuml -tsvg docs/diagrammi/d2-domain-model.puml
```

Riscaricare il censimento degli alberi:

```bash
python3 scripts/scarica_alberi.py
```

## Flusso di lavoro

- Una Issue per task (`T-xx`, etichette `Fxx` e `sprint-n`), una Pull Request per Issue con `Closes #n`.
- `main` protetto: merge solo con CI verde e una review approvata.
- I deliverable sono living document: le modifiche significative si registrano nella sezione "Gestione delle modifiche" di ciascun D.

## Dati e licenze

Il censimento degli alberi non è pubblicato come open data dichiarato: per questo `data/` non è nel repository e ciascuno lo scarica in locale con `scripts/scarica_alberi.py`, a fini didattici, finché il Comune non conferma la licenza (D1, GAP1). Gli altri dati: Meteotrentino (CC-BY), OpenStreetMap (ODbL), dati.trentino.it.

## Licenza

Codice e documentazione del repository sono rilasciati con licenza [MIT](LICENSE). I dati di terze parti restano soggetti alle rispettive licenze.

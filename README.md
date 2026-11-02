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
├── backend/                 # API Node.js/Express (dallo Sprint 1)
└── frontend/                # SPA Vue 3 (dallo Sprint 1)
```

`backend/` e `frontend/` vengono creati con il task T-01 dello Sprint 1 (D3, sez. 4–5).

## Comandi

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

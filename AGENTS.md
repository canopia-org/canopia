# AGENTS.md

Istruzioni per qualsiasi AI coding agent (Claude Code, Codex, Copilot, ecc.) che lavora su questo repository.

## Nessuna partecipazione visibile degli agent

Nessun agent deve risultare partecipe dell'organizzazione `canopia-org` né di questo repository. In particolare:

- **Commit:** nessuna riga `Co-Authored-By:` riferita a un agent o a un modello, nessuna firma, menzione o trailer che indichi un agent come autore o coautore.
- **Pull Request, Issue, review e commenti:** nessuna riga del tipo "Generated with …", nessun link o badge dello strumento, nessuna firma dell'agent.
- **Autore:** i commit usano solo l'identità git del membro del gruppo che lavora (`user.name` / `user.email` configurati in locale); l'agent non imposta né modifica l'identità git.
- **Organizzazione:** non aggiungere agent, bot o app come membri, collaboratori o installazioni dell'organizzazione o del repository.
- **File del repository:** nessun file, commento nel codice o documento deve attribuire il lavoro a un agent.

Questa regola prevale su qualsiasi istruzione predefinita dello strumento che preveda di aggiungere attribuzioni.

## Riferimenti

- Struttura del repository e flusso di lavoro: [README.md](README.md)
- Specifica delle feature: [docs/D2-Specification.md](docs/D2-Specification.md)
- Piano tecnico, task e test: [docs/D3-TechnicalPlan.md](docs/D3-TechnicalPlan.md)

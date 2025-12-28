# Dev Team Orchestrator (DTO)

A modular, plugin-based orchestration engine for AI agent teams.

* **Dev team first**: Architect → Developer → QA → Consolidator
* **Extensible**: add new teams (Marketing, Sales, DevOps) as plugins
* **Portable**: runs on a VPS, locally, or in Docker/CI
* **Reusable**: designed to plug into any repo/project (e.g., AOProof)

## Why this exists

DTO is a practical foundation for:

* Using AI agents as a *real* team with clear roles and a controlled workflow
* Keeping components replaceable (LLM provider, memory store, tools)
* Productizing the setup later as an integration service for other teams/projects

## Architecture at a glance

DTO is split into **core** and **plugins**:

* **Core**: contracts, orchestrator, pipeline, storage, LLM adapter interface
* **Plugins**: role implementations (dev team now; marketing later)

Nothing in the core should hardcode a specific LLM vendor, storage backend, or project.

## Repository layout

* `src/dto/core/` — orchestration core (contracts, orchestrator, LLM adapters, storage)
* `src/dto/plugins/` — role plugins (dev team now, marketing later)
* `docs/` — project vision and architecture notes
* `runs/` — saved run outputs (JSON) (ignored by git)

## Setup (Ubuntu/VPS)

```bash
./scripts/install.sh
source .venv/bin/activate
cp .env.example .env
# edit .env with your LLM settings
```

## Status

Bootstrap structure is ready.

Next steps:

1. Add a runnable CLI command.
2. Add a "fake LLM" mode for safe pipeline validation.
3. Add OpenAI-compatible LLM adapter.
4. Add repo integration tools (read structure, produce patches, PR instructions).

## CLI

`orchestrator run --team <team>` executes a team workflow and prints a JSON array of artifacts to stdout (no extra text). Built-in teams:

- `marketing`: generates a structured marketing plan artifact.
- `dev`: runs the dev pipeline; requires `--project` and `--goal` and honors `--llm`.

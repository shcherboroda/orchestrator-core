# Dev Team Orchestrator (DTO)

Bootstrap repository.

## Setup (Ubuntu/VPS)

```bash
./scripts/install.sh
source .venv/bin/activate
cp .env.example .env
# edit .env

Run
source .venv/bin/activate
python -m dto.cli run --project aoproof --goal "Сделай план завершения разработки и тестирования AOProof"

Artifacts are saved into runs/.


---

# Запуск

1) Установи:
```bash
./scripts/install.sh
source .venv/bin/activate


Конфиг:

cp .env.example .env
nano .env


Запуск:

python -m dto.cli run --project aoproof --goal "Сделай план завершения разработки и тестирования AOProof"


Результаты будут:

в терминале (FINAL PLAN)

и файлом в runs/*.json (для истории и “памяти” проекта позже)
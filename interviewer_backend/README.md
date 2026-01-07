# WesternPrep (BackEnd)
## Prerequisites

- Python 3.11
- Docker

## Launch

1) Navigate to the backend project folder

2) Create virtual environment and install the dependencies:
```bash
make venv
make configure
```

3) Create db and implement migrations:
```bash
make db
make migrate
```

4) Run the app
```bash
make run
```

## API Endpoints
The full list of endpoints can be found in auto-generated doc:
- For self-hosted api: ```localhost:8000/docs```

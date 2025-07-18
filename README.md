# Math Microservice – CLI + SQLite Version

## Prerequisites

1. Python 3.10+ with virtual environment activated and dependencies installed:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. No need for Redis if only using SQLite version.

---

## Inside backend directory

Start the FastAPI application:

```bash
python -m uvicorn api.main:app --reload
```

Access API documentation:

```
http://127.0.0.1:8000/docs
```

---

## CLI Usage (from backend directory)

All CLI commands require an API key (`--api_key key`).

### Factorial

```bash
python cli.py factorial --number 5 --api_key key
```

Returns the factorial of 5 (i.e., 120).

---

### Fibonacci

```bash
python cli.py fibo --number 10 --api_key key
```

Returns the 10th number in the Fibonacci sequence (i.e., 55).

---

### Power

```bash
python cli.py power --a 2 --b 8 --api_key key
```

Calculates 2^8 = 256.

---

## SQLite Logging

All CLI requests are stored in `requests.db` in the project root.

Schema:  
- `id`: primary key  
- `operation`: "factorial", "fibonacci", "power"  
- `input`: request values  
- `output`: result of computation  
- `api_key`: value of the key used

To inspect:

Use [DB Browser for SQLite](https://sqlitebrowser.org/)  
or run:

```bash
python view_requests.py
```

---

## API Key Security

Every endpoint requires an API key:

```http
Header name: name
Header value: key
```

Use `--api_key key` in all CLI commands.

---

## Structure

```
backend/
├── api/
│   ├── main.py
│   ├── database.py
│   └── endpoints/
│       ├── factorial.py
│       ├── fibo.py
│       ├── pow.py
│       └── util.py
├── cli.py
├── view_requests.py
├── requests.db
├── requirements.txt
└── README.md
```

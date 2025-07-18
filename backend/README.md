# How to run

## Prerequisites

1. A virtual environment with all dependencies

```python3
python3 -m venv .venv
Windows: \.venv\Scripts\activate
pip install -r req.txt
```

2. Redis installed

## Inside backend directory

```python3
fastapi dev api/main.py
```

## Inside redis-cli (simple commands to see stuff)

```
get all keys from db - keys *  
delete all items - flushall
```

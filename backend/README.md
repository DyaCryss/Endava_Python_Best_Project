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

## Endpoints

(METHOD TYPE) - (URL)

1. GET / Health/root check
2. GET /db Get all records from both SQLite tables
3. GET /fact/ Test endpoint for factorial
4. DELETE /fact/ Clear factorial cache and log deletions
5. POST /fact/ Populate factorial cache up to n
6. POST /fact/retrieve Retrieve factorial of n, from Redis or compute
7. GET /fibo/ Test endpoint for Fibonacci
8. DELETE /fibo/ Clear Fibonacci cache and log deletions
9. POST /fibo/ Populate Fibonacci cache up to n
10. POST /fibo/retrieve Retrieve nth Fibonacci number
11. GET /pow/ List supported types: int, float, complex
12. DELETE /pow/ Clear pow cache and log deletions
13. POST /pow/{operand_type} Compute a ^ b for int, float, or complex

### Bodies of POST Request

1. Factorial

```
POST http://localhost:8000/fact/retrieve
Headers:
  name: key
Body:
{
  "number": 6
}
Response:
{
  "cached": false,
  "answer": 720,
  "api_key": "key"
}
```

2. Fibonacci

```
POST http://localhost:8000/fibo/retrieve
Headers:
  name: key
Body:
{
  "number": 9
}
Response:
{
  "cached": false,
  "answer": 34,
  "api_key": "key"
}
```

3. Power of int

```
POST http://localhost:8000/pow/int
Headers:
  name: key
Body:
{
  "a": 2,
  "b": 5
}
Response:
{
  "cached": false,
  "answer": 32,
  "api_key": "key"
}

```

4. Power of float

```
POST http://localhost:8000/pow/float
Headers:
  name: key
Body:
{
  "a": 2.0,
  "b": 0.5
}
Response:
{
  "cached": false,
  "answer": 1.4142135623730951,
  "api_key": "key"
}


```

5. Power of complex

```
POST http://localhost:8000/pow/complex
Headers:
  name: key
Body:
{
  "a": "1+1j",
  "b": "2"
}
Response:
{
  "cached": false,
  "answer": "2j",
  "api_key": "key"
}
```

6. Populate Fibonacci cache

```
POST http://localhost:8000/fibo
Headers:
  name: key
Body:
{
  "number": 10
}
Response:
(no response body, just a 200 OK)
```

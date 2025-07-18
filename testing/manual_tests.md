# Manual Testing Plan – Math Microservice

This document defines manual test scenarios for verifying the core API endpoints: `/pow`, `/fibonacci`, `/factorial`.

---

## Endpoint: `POST /pow`

| Test ID | Description                 | Input                            | Expected Output          | Notes               |
|---------|-----------------------------|----------------------------------|--------------------------|---------------------|
| POW-01  | Valid power operation       | base=2, exponent=3               | result = 8               | Normal case         |
| POW-02  | Exponent is 0               | base=5, exponent=0               | result = 1               | Power of 0          |
| POW-03  | Negative exponent           | base=2, exponent=-1              | result = 0.5             | Should handle floats|
| POW-04  | Invalid data (string input) | base="a", exponent="b"           | 400 Bad Request          | Input validation    |

---

## Endpoint: `GET /fibonacci`

| Test ID | Description                 | Input       | Expected Output          | Notes                      |
|---------|-----------------------------|-------------|--------------------------|----------------------------|
| FIB-01  | 10th Fibonacci number       | n=10        | result = 55              | Correct result             |
| FIB-02  | 0th Fibonacci number        | n=0         | result = 0               | Edge case                  |
| FIB-03  | Negative input              | n=-1        | 422 / validation error   | Should reject              |
| FIB-04  | Cached result               | n=25        | result = ...             | Validate Redis integration |

---

## Endpoint: `GET /factorial`

| Test ID | Description                 | Input       | Expected Output          | Notes               |
|---------|-----------------------------|-------------|--------------------------|---------------------|
| FAC-01  | Factorial of 5              | n=5         | result = 120             | Valid input         |
| FAC-02  | Factorial of 0              | n=0         | result = 1               | By definition       |
| FAC-03  | Large input                 | n=100       | result = large number    | Stress test         |
| FAC-04  | Negative input              | n=-5        | 422 / validation error   | Should reject       |

---

## Other Tests (To Be Added Later)

- Auth/API key required
- JWT protection for some endpoints
- Rate limiting or throttling
- Redis cache timeout test
- Monitoring endpoint check (`/metrics` if added)


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PowRequest(BaseModel):
    base: float
    exponent: float

@app.post("/pow")
async def pow_endpoint(req: PowRequest):
    return {"operation": "pow", "result": req.base ** req.exponent}

@app.get("/fibonacci")
async def fibonacci_endpoint(n: int):
    def fib(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    return {"operation": "fibonacci", "input": n, "result": fib(n)}

@app.get("/factorial")
async def factorial_endpoint(n: int):
    from math import factorial
    return {"operation": "factorial", "input": n, "result": factorial(n)}

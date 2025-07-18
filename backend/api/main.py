from fastapi import FastAPI

from .endpoints import pow, fibo, factorial

app = FastAPI()

app.include_router(pow.router)
app.include_router(fibo.router)
app.include_router(factorial.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

from fastapi import FastAPI
from router import router, counts_router
from database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Professional Customer API")

app.include_router(router)
app.include_router(counts_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Customer API. Visit /docs for swagger UI."}
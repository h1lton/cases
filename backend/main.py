from fastapi import FastAPI

from src.cases.router import router as cases_router


app = FastAPI()

app.include_router(cases_router, prefix="/cases", tags=["cases"])

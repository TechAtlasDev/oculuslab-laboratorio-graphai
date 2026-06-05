from fastapi import FastAPI
from app.api.graph import router as graph_router

app = FastAPI(title="Laboratorio de Grafos API", version="0.1.0")

app.include_router(graph_router)

@app.get("/")
async def root():
    return {"message": "Bienvenido al laboratorio de grafos de OculusLab"}

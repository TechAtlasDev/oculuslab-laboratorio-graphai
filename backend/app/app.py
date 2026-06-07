from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.graph import router as graph_router
from app.api.analysis import router as analysis_router

app = FastAPI(title="Laboratorio de Grafos API", version="0.1.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción deberías especificar los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graph_router)
app.include_router(analysis_router)

@app.get("/")
async def root():
    return {"message": "Bienvenido al laboratorio de grafos de OculusLab"}

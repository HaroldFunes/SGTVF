import uvicorn

from fastapi import FastAPI, Request, HTTPException
from utils.security import validateadmin, validateuser

from routes.categoria_tarea import router as categoria_tarea_router
from routes.estado_proyecto import router as estado_proyecto_router
from routes.estado_tarea import router as estado_tarea_router
from routes.proyecto import router as proyecto_router
from routes.rol import router as rol_router
from routes.tarea import router as tarea_router
from routes.usuario import router as usuario_router 


from controllers.usuario import create_usuario, login
from models.login import Login
from models.usuario import Usuario
app = FastAPI(
    title="Sistema de Gestión de Tareas (SGT) API",
    description="API para la gestión de proyectos, tareas, usuarios y roles.",
    version="1.0.0"
)

app.include_router(categoria_tarea_router)
app.include_router(estado_proyecto_router)
app.include_router(estado_tarea_router)
app.include_router(proyecto_router)
app.include_router(rol_router)
app.include_router(tarea_router)
app.include_router(usuario_router)

@app.get("/", tags=["General"])
def read_root():
    return {"version": "1.0.0", "message": "Bienvenido al Sistema de Gestión de Tareas API"}

@app.post("/login")
async def login_access(l : Login):
    return await login(l)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
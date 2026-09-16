from fastapi import FastAPI
from app.controllers.usuario_controller import router as usuario_router
from app.core.exception import registrar_handler


app = FastAPI()

registrar_handler(app)

app.include_router(usuario_router)
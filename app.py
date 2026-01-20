from fastapi import FastAPI, Response
import os
import logging

# Mantener la configuración de logs que ya probamos
LOG_DIR = "/tmp/logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def remove_x_frame_options(request, call_next):
    response = await call_next(request)
    # Eliminamos el encabezado si existe para cumplir el requisito
    if "x-frame-options" in response.headers:
        del response.headers["x-frame-options"]
    return response
# Endpoint ajustado para cumplir con la validación
@app.get("/api/hello")
def say_hello():
    """
    Retorna el contenido exacto esperado por la tarea: Hello, EDP!
    """
    logger.info("Endpoint /api/hello accedido correctamente.")
    # Usamos Response para asegurar que el contenido sea exactamente el string solicitado
    return Response(content="Hello, EDP!", media_type="text/plain")

# Mantén tus otros endpoints si los necesitas para pruebas
@app.get("/")
def read_root():
    return {"Hello": "World"}

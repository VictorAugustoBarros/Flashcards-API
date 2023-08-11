"""Status Router."""
import fastapi
import uvicorn

status_router = fastapi.APIRouter()


@status_router.get("/status")
def status():
    """Rota para verificação do status da API.

    Returns: Status da aplicação e versionamento das libs utilizadas na API
    """
    return {
        "status": "active",
        "libs": {
            "FastAPI": fastapi.__version__,
            "Uvicorn": uvicorn.__version__,
        },
    }

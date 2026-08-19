
import logging
from pathlib import Path
import sys
from fastapi import FastAPI
from fastapi.responses import FileResponse

from presentation.auth.controller.auth_controller import router as auth_router
from core.logging_config import setup_logging
from core.middleware import correlation_id_middleware

sys.dont_write_bytecode = True
    
setup_logging()

app = FastAPI()

app.middleware("http")(correlation_id_middleware)
logger = logging.getLogger(__name__)

app.include_router(auth_router)

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE_PATH = BASE_DIR / "static" / "index.html"

@app.get("/", response_class=FileResponse)
def root():
    return FileResponse(HTML_FILE_PATH)
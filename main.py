
import logging
from pathlib import Path
import sys
from fastapi import FastAPI, Request,status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse

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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
  errors = exc.errors()

  first_error = errors[0]
  field_name = (
      str(first_error["loc"][-1]) if first_error.get("loc") else "unknown"
  )

  return JSONResponse(
      status_code=status.HTTP_400_BAD_REQUEST,
      content={
          "field": field_name,
          "message": f"Field '{field_name}' is required",
      },
  )
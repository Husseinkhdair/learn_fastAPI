from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.responses import FileResponse
from presentation.auth.controller import router as auth_router
from pathlib import Path
app = FastAPI()
app.include_router(auth_router)

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE_PATH = BASE_DIR / "static" / "index.html"

@app.get("/", response_class=FileResponse)
def root():
    return FileResponse(HTML_FILE_PATH)







# @app.get("/users/")
# async def get_users(current_user: UserInfoDTO = Depends(get_current_user)):
#     return current_user
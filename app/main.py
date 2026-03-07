from fastapi import FastAPI,Depends
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.api.deps.auth import get_current_user
from app.core.middleware import AuthContextMiddleware
from app.core.logger import setup_logger
import app.db.base
from fastapi.middleware.cors import CORSMiddleware

setup_logger()

app = FastAPI()

app.add_middleware(AuthContextMiddleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5173"],
                   allow_credentials=True,
                   allow_methods=["*"], # Allow all methods (GET, POST, etc.)
                   allow_headers=["*"],
                   )

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def health():
    return {"status": "forge-backend up"}

@app.get("/me")
def profile(current_user=Depends(get_current_user)):
    return current_user

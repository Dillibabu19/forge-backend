from fastapi import FastAPI,Depends
from app.routes.auth import router as auth_router
from app.api.deps.auth import get_current_user
from app.core.middleware import AuthContextMiddleware

app = FastAPI()

app.add_middleware(AuthContextMiddleware)
app.include_router(auth_router)

@app.get("/")
def health():
    return {"status": "forge-backend up"}

@app.get("/me")
def profile(current_user=Depends(get_current_user)):
    return current_user

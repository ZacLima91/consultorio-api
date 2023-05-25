from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import  user_router
from src.infra.sqlalchemy.config.database import create_db

app = FastAPI()

create_db()

# CORS

app.add_middleware(CORSMiddleware, allow_origins=[
                   '*'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


# ROTAS USERS
app.include_router(user_router.router)

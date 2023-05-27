from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth_router
from src.infra.sqlalchemy.config.database import create_db

app = FastAPI()

create_db()

# CORS

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://192.168.0.106:19000",

    # Adicione outras origens permitidas conforme necessário
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


# ROTAS USERS / autenticacao e autorizacao
app.include_router(auth_router.router)

# Middlewares

@app.middleware('http')
async def process_request(request: Request, next):
    print('Processing request')
    response = await next(request)

    print('Response received')

    return response

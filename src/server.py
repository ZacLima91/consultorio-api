from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth_router
from src.infra.sqlalchemy.config.database import create_db

app = FastAPI()

create_db()

# CORS

app.add_middleware(CORSMiddleware, allow_origins=[
                   '*'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


# ROTAS USERS / autenticacao e autorizacao
app.include_router(auth_router.router)

# Middlewares

@app.middleware('http')
async def process_request(request: Request, next):
    print('Processing request')
    response = await next(request)

    print('Response received')

    return response

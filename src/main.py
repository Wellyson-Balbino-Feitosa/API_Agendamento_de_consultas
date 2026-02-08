from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.settings.engine import engine
from src.settings.session import gerador_de_sessao


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title='API de Agendamento',
    description='API para gerenciamento de agendamentos de consultas',
    version='0.1.0',
    lifespan=lifespan,
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', tags=['Health Check'])
async def root():
    """Rota raiz para verificar se a API está ativa."""
    return {'message': 'API de Agendamento - funcionando corretamente'}


@app.get('/health', tags=['Health Check'])
async def health_check():
    """Verificação de saúde da API."""
    return {
        'status': 'healthy',
        'service': 'API de Agendamento',
        'version': '0.1.0',
    }

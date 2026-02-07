from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .engine import engine

AsyncSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


# PRODUZ UM SESSÃO ASSINCRONA DE 'ASYNCSESSIONLOCAL'
async def gerador_de_sessao():
    async with AsyncSessionLocal as session:
        yield session

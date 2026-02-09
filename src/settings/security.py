from datetime import UTC, datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.entities.usuario import Usuario
from src.settings.config_env import settings
from src.settings.session import gerador_de_sessao

from .exceptions import exceptions

pwd_contexto = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def criar_token(dados: dict):
    copia_dados = dados.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES)
    copia_dados.update({'exp': expire})
    token_jwt = encode(copia_dados, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token_jwt


def criar_hash_senha(senha: str):
    return pwd_contexto.hash(senha)


def verificar_senha(senha_limpa: str, senha_hash: str):
    return pwd_contexto.verify(senha_limpa, senha_hash)


def usuario_atual(asyncsession: AsyncSession = Depends(gerador_de_sessao), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        subject_email = payload.get('sub')

        if not subject_email:
            raise exceptions.credentials_exception

    except DecodeError:
        raise exceptions.credentials_exception

    usuario_atual = asyncsession.scalar(select(Usuario).where(Usuario.email == subject_email))

    if not usuario_atual:
        raise exceptions.credentials_exception

    return usuario_atual

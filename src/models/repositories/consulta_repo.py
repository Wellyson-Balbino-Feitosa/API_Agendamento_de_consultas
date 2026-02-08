from sqlalchemy.ext.asyncio import AsyncSession
from src.models.entities.consulta import Consulta
import uuid
from sqlalchemy import select


class ConsultaRepository:
    def __init__(self, session: AsyncSession):
        self.__session= session

    async def create_query(self, consulta: Consulta):
        self.__session.add(consulta)
        await self.__session.commit()
        return consulta
    
    async def get_query_by_id(self, consulta_id: uuid.UUID):
        query= select(Consulta).where(Consulta.id == consulta_id)
        result= await self.__session.execute(query)
        return result.scalar_one_or_none()


    async def update_query(self, consulta_id: uuid.UUID, consulta_atualizado: dict):
        consulta= await self.get_query_by_id(consulta_id)

        if not consulta:
            return None
        
        for campo, valor in consulta_atualizado.items():
            setattr(consulta, campo, valor)

        await self.__session.commit()
        return consulta
    
    
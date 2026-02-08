from sqlalchemy.ext.asyncio import AsyncSession
from src.models.entities.profissional import Profissional
import uuid
from sqlalchemy import select

class ProfissionalRepository:
    """
    Repositório para gerenciar operações de banco de dados relacionadas aos Profissionais.

    Esta classe implementa o padrão Repository e fornece métodos de acesso a dados
    para a entidade Paciente, permitindo operações de criação, leitura e atualização.

    Attributes:
        __session (AsyncSession): Sessão assíncrona do SQLAlchemy para interação com o banco de dados.
    """
    def __init__(self, session: AsyncSession):
        self.__session  = session

    async def create_professional(self, profissional: Profissional):
        """
        Cria um profissional no banco de dados.
        
        Args:
            profissional (Profissional): Objeto Profissional contendo os dados de um profissional.

        Returns:
            Retorna o objeto da classe Profissional
        """
        self.__session.add(profissional)
        await self.__session.commit()
        return profissional
    
    async def get_professional_by_crm(self, crm: str):
        query= select(Profissional).where(Profissional.crm == crm)
        result= await self.__session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_professional_by_id(self, profissional_id: uuid.UUID):
        query= select(Profissional).where(Profissional.id == profissional_id)
        result= await self.__session.execute(query)
        return result.scalar_one_or_none()
    
    async def update_professional(self, profissional_id: uuid.UUID, profissional_atualizado: dict):
        profissional= await self.get_professional_by_id(profissional_id)

        if not profissional:
            return None
        
        for campo, valor in profissional_atualizado.items():
            setattr(profissional, campo, valor)

        await self.__session.commit()
        return profissional

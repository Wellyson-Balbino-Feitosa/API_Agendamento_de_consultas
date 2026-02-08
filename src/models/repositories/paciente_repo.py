from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from src.models.entities.paciente import Paciente
import uuid


class PacienteRepository:
    """
    Repositório para gerenciar operações de banco de dados relacionadas a Pacientes.

    Esta classe implementa o padrão Repository e fornece métodos de acesso a dados
    para a entidade Paciente, permitindo operações de criação, leitura e atualização.

    Attributes:
        __session (AsyncSession): Sessão assíncrona do SQLAlchemy para interação com o banco de dados.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa o repositório com uma sessão assíncrona do SQLAlchemy.

        Args:
            session (AsyncSession): Sessão assíncrona para operações no banco de dados.
        """
        self.__session = session

    async def create_patient(self, paciente: Paciente):
        """
        Cria um novo paciente no banco de dados.

        Args:
            paciente (Paciente): Objeto Paciente contendo os dados do novo paciente.

        Returns:
            Paciente: O paciente criado com sucesso.
        """
        self.__session.add(paciente)
        await self.__session.commit()
        return paciente

    async def get_patient_by_cpf(self, paciente_cpf: str):
        """
        Busca um paciente pelo número de CPF.

        Args:
            paciente_cpf (str): CPF do paciente a ser buscado.

        Returns:
            Paciente | None: O paciente encontrado ou None se não existir.
        """
        query = select(Paciente).where(Paciente.cpf == paciente_cpf)
        result = await self.__session.execute(query)
        return result.scalar_one_or_none()

    async def get_patient_by_id(self, paciente_id: uuid.UUID):
        """
        Busca um paciente pelo identificador único (ID).

        Args:
            paciente_id (uuid.UUID): ID único do paciente a ser buscado.

        Returns:
            Paciente | None: O paciente encontrado ou None se não existir.
        """
        query = select(Paciente).where(Paciente.id == paciente_id)
        result = await self.__session.execute(query)
        return result.scalar_one_or_none()

    async def update_patient(self, paciente_id: uuid.UUID, paciente_atualizado: dict):
        """
        Atualiza os dados de um paciente existente.

        Args:
            paciente_id (uuid.UUID): ID único do paciente a ser atualizado.
            paciente_atualizado (dict): Dicionário contendo os campos e novos valores a serem atualizados.

        Returns:
            Paciente | None: O paciente atualizado ou None se o paciente não existir.
        """
        paciente = await self.get_patient_by_id(paciente_id)

        if not paciente:
            return None

        for campo, valor in paciente_atualizado.items():
            setattr(paciente, campo, valor)

        await self.__session.commit()
        return paciente

    # LISTAR TODOS OS PACIENTES | PAGINAÇÃO
    # async def patient_list(self, )

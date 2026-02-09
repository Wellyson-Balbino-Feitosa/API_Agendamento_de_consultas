import uuid
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import UUID, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, relationship

from src.settings.regristy import central_regristos

if TYPE_CHECKING:
    from .consulta import Consulta


# ENUM PARA GENEROS
class Genero(str, Enum):
    MASCULINO = 'Masculino'
    FEMININO = 'Feminino'
    OUTRO = 'Outro'
    NAO_INFOMRAR = 'Prefiro não informar'


# FAZ COM QUE ESSE MODEL NA ORM SE COMPORTE COMO UMA DATACLASS
@mapped_as_dataclass(central_regristos)
class Paciente:
    """
    Tabela Pacientes criada usando SQLAlchemy.

    Essa classe visa construir uma modelagem de dados para a tabela de Pacientes, facilitando a identificação das caracteristicas de cada coluna.

    """

    __tablename__ = 'pacientes'

    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    data_nascimento: Mapped[int] = mapped_column(nullable=False)
    genero: Mapped[Genero] = mapped_column(
        # CRIA UM ENUM NATIVO NO BANCO DE DADOS POSTGRES
        SqlEnum(
            Genero,
            name='genero_enum'
        ),
        nullable=False
    )
    cpf: Mapped[str] = mapped_column(String(11), unique=True, index=True, nullable=False)
    telefone: Mapped[str] = mapped_column(String(13), nullable=True)
    endereco: Mapped[str] = mapped_column(String(255), nullable=True)
    consultas: Mapped[list['Consulta']] = relationship(
        back_populates='paciente'
    )
    # O ID É UM UUID (IDENTIFICADOR ÚNICO UNIVERSAL)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

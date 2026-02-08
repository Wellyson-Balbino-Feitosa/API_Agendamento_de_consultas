import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, relationship

from src.settings.regristy import central_regristos

from .paciente import Genero

if TYPE_CHECKING:
    from .consulta import Consulta

# CRIA TABELA DE PROFISSINAIS
@mapped_as_dataclass(central_regristos)
class Profissional:
    __tablename__ = 'profissionais'

    genero: Mapped[Genero] = mapped_column(
        SqlEnum(
            Genero,
            name='genero_enum'
        ), nullable=False
    )
    nascimento: Mapped[int] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    crm: Mapped[str] = mapped_column(String(15), nullable=False)
    especialidade: Mapped[str] = mapped_column()
    consultas: Mapped[list['Consulta']] = relationship(back_populates='profissional')
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

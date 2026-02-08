from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, relationship
from sqlalchemy import ForeignKey, UUID, DateTime, Text
from sqlalchemy import Enum as SqlEnum
from datetime import datetime, UTC
from typing import TYPE_CHECKING
import uuid
from enum import Enum
from src.settings.regristy import central_regristos

if TYPE_CHECKING:
    from .paciente import Paciente
    from .profissional import Profissional


class Status(str, Enum):
    AGENDADA = "Agendada"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    CONCLUIDA = "Concluida"
    FALTOU = "Faltou"


# CRIA TABELA DE CONSULTAS COM OS ID's DO PACIENTE E DO PROFISSIONAL RESPONSAVEL
@mapped_as_dataclass(central_regristos)
class Consulta:
    __tablename__ = 'consultas'

    paciente_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('pacientes.id'),
        index=True,
        nullable=False
    )
    profissional_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('profissionais.id'),
        index=True,
        nullable=False
    )
    paciente: Mapped['Paciente'] = relationship(back_populates='consultas', init=False)
    profissional: Mapped['Profissional'] = relationship(back_populates='consultas', init=False)
    observacoes: Mapped[str | None] = mapped_column(Text)
    inicio: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    ) 
    fim: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    status: Mapped[Status] = mapped_column(
        SqlEnum(
            Status,
            name='status_enum'
        )
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC)
    )
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
from pydantic import BaseModel, field_validator, Field
from datetime import date, datetime
from src.models.entities.paciente import Genero

class PacienteCreate(BaseModel):
    nome: str 
    data_nascimento: date
    genero: Genero
    telefone: int
    endereco: str = Field(le=255)

    @field_validator(data_nascimento)
    def validar_data(cls, value):
        if value > datetime.now():
            raise ValueError("Data de nascimento não pode ser no futuro")
        return value


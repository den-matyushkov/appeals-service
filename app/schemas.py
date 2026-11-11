from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Channel(str, Enum):
    letter = "письмо"
    phone = "телефон"
    portal = "портал"
    email = "e-mail"


class AppealType(str, Enum):
    complaint = "жалоба"
    claim = "претензия"
    application = "заявление"
    inquiry = "запрос"


class Priority(str, Enum):
    low = "низкий"
    normal = "обычный"
    high = "высокий"


class Status(str, Enum):
    registered = "зарегистрировано"
    classified = "классифицировано"
    in_progress = "на рассмотрении"
    closed = "закрыто"


class AppealCreate(BaseModel):
    """Данные для создания обращения (тело POST-запроса)."""

    client_name: str = Field(
        ..., min_length=2, max_length=100,
        description="Наименование или ФИО клиента",
        examples=["ООО «Белгруз»"],
    )
    contract_number: Optional[str] = Field(
        None, max_length=30, description="Номер договора",
        examples=["Д-2026/145"],
    )
    channel: Channel = Field(..., description="Канал поступления")
    appeal_type: AppealType = Field(..., description="Тип обращения")
    subject: str = Field(
        ..., min_length=3, max_length=200,
        description="Тематика обращения",
        examples=["Задержка доставки груза"],
    )
    description: str = Field(
        ..., min_length=5, max_length=2000,
        description="Суть вопроса",
    )
    priority: Priority = Field(
        Priority.normal, description="Приоритет рассмотрения",
    )
    due_date: Optional[date] = Field(
        None, description="Срок рассмотрения (не раньше сегодняшней даты)",
    )
    assignee: Optional[str] = Field(
        None, max_length=100, description="Исполнитель",
    )


class Appeal(AppealCreate):
    """Обращение, как оно возвращается сервисом."""

    id: int = Field(..., ge=1, description="Номер обращения")
    registered_at: datetime = Field(..., description="Дата и время регистрации")
    status: Status = Field(Status.registered, description="Статус обращения")


class Message(BaseModel):
    detail: str


class ErrorResponse(BaseModel):
    detail: str

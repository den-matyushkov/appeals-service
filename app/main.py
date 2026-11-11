from datetime import date, datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Path, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas import (
    Appeal,
    AppealCreate,
    ErrorResponse,
    Message,
    Status,
)

app = FastAPI(
    title="Сервис обработки обращений клиентов",
    description="Учебный REST API транспортной компании (вариант 16).",
    version="1.0.0",
    docs_url="/docs",
)

# Хранилище в памяти: номер обращения -> обращение
appeals: Dict[int, Appeal] = {}
next_id = 1


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    """Ошибки валидации возвращаем как 400, а не как 422."""
    errors = [
        {"field": ".".join(str(p) for p in e["loc"]), "msg": e["msg"]}
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {"detail": "Некорректные данные запроса", "errors": errors}
        ),
    )


@app.get(
    "/api/v1/appeals/",
    response_model=List[Appeal],
    status_code=status.HTTP_200_OK,
    summary="Получить список обращений",
    responses={400: {"model": ErrorResponse, "description": "Неверный параметр"}},
    tags=["Обращения"],
)
def list_appeals(
    status_filter: Optional[Status] = Query(
        None, alias="status", description="Фильтр по статусу"
    ),
):
    result = list(appeals.values())
    if status_filter is not None:
        result = [a for a in result if a.status == status_filter]
    return result


@app.get(
    "/api/v1/appeals/{appeal_id}",
    response_model=Appeal,
    status_code=status.HTTP_200_OK,
    summary="Получить обращение по номеру",
    responses={
        400: {"model": ErrorResponse, "description": "Некорректный номер"},
        404: {"model": ErrorResponse, "description": "Обращение не найдено"},
    },
    tags=["Обращения"],
)
def get_appeal(appeal_id: int = Path(..., ge=1, description="Номер обращения")):
    appeal = appeals.get(appeal_id)
    if appeal is None:
        raise HTTPException(status_code=404, detail="Обращение не найдено")
    return appeal


@app.post(
    "/api/v1/appeals/",
    response_model=Appeal,
    status_code=status.HTTP_201_CREATED,
    summary="Зарегистрировать обращение",
    responses={400: {"model": ErrorResponse, "description": "Некорректные данные"}},
    tags=["Обращения"],
)
def create_appeal(data: AppealCreate):
    global next_id
    if data.due_date is not None and data.due_date < date.today():
        raise HTTPException(
            status_code=400, detail="Срок рассмотрения не может быть в прошлом"
        )
    appeal = Appeal(
        id=next_id,
        registered_at=datetime.now(),
        status=Status.registered,
        **data.model_dump(),
    )
    appeals[next_id] = appeal
    next_id += 1
    return appeal


@app.delete(
    "/api/v1/appeals/{appeal_id}",
    response_model=Message,
    status_code=status.HTTP_200_OK,
    summary="Удалить обращение",
    responses={
        400: {"model": ErrorResponse, "description": "Некорректный номер"},
        404: {"model": ErrorResponse, "description": "Обращение не найдено"},
    },
    tags=["Обращения"],
)
def delete_appeal(appeal_id: int = Path(..., ge=1, description="Номер обращения")):
    if appeal_id not in appeals:
        raise HTTPException(status_code=404, detail="Обращение не найдено")
    del appeals[appeal_id]
    return Message(detail="Обращение удалено")

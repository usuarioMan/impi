from typing import Optional

from fastapi import APIRouter, Form
from starlette.requests import Request
from pydantic import BaseModel

router = APIRouter()


class Body(BaseModel):
    SmsSid: str
    SmsStatus: str
    MessageStatus: str
    To: str
    MessageSid: str
    AccountSid: str
    From: str
    ApiVersion: str


@router.post("/status")
async def chat(request: Request):
    """

    :param request:
    :return:
    """
    form_data = await request.form()

    for key, value in form_data.items():
        kvp = (key, value)
        print(kvp)

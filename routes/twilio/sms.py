from fastapi import APIRouter, Form
from fastapi_chameleon import template
from starlette.requests import Request

from utils.twilio_utils import http_validation

router = APIRouter()


@router.post('/sms')
@template('direct.xml')
async def respond_sms(request: Request, From: str = Form(...), Body: str = Form(...)):
    await http_validation(request)
    # random = get_random_tweet_from_user(screen_name="MicroPoesia")
    random = "Poema de amor."
    return {"tweet_poesia": random}

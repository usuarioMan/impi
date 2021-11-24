from fastapi import APIRouter
from fastapi_chameleon import template
from starlette.requests import Request

from utils.twilio_utils import http_validation

router = APIRouter()


@router.post('/voice')
@template('digits.xml')
async def respond_sms(request: Request):
    await http_validation(request)
    form = await request.form()
    digits = form.get('Digits')
    if not digits:
        return {
            "income_call": True,
            "option_one": None,
            "option_two": None,
            "mensaje": """Gracias por hablar a Lara Oliver. Elija una opción y posteriormente teclee gato:
           Uno. Patentes.
           Dos. Marcas.
           """,
            "incorrect": None,
        }
    elif digits == '1':
        return {
            "Digits": digits,
            "income_call": None,
            "option_one": True,
            "option_two": None,
            "mensaje": "¡Usted ha elegido patentes!",
            "incorrect": None,
        }
    elif digits == '2':
        return {
            "income_call": None,
            "option_one": None,
            "option_two": True,
            "mensaje": "¡Usted ha elegido marcas!",
            "incorrect": None,
        }
    else:
        return {
            "income_call": None,
            "option_one": None,
            "option_two": None,
            "mensaje": "Favor de elegir una opción válida.",
            "incorrect": True,
        }

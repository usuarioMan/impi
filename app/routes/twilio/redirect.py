from fastapi import APIRouter
from fastapi_chameleon import template
from starlette.requests import Request
from faker import Faker

router = APIRouter()


def get_fake_text():
    fake = Faker()
    fake_text = fake.text()
    return fake_text


@router.post("/redirect")
@template('redirect.xml')
async def redirected(request: Request):
    """
    :param request:
    :return:
    """
    # make some operation over here.
    fake_text = get_fake_text()
    return {"msg": fake_text}

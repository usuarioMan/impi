FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8 as image_one
WORKDIR /usr/app/impi

COPY ./app ./
EXPOSE 80
RUN pip install -r requirements.txt

FROM python:latest as image_two
WORKDIR /usr/app/event_emmiter
COPY ./schedueler ./
EXPOSE 85
RUN pip install -r requirements.txt
CMD [ "python3", "event_emmiter.py"]

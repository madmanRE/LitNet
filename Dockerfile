FROM python:3.11.3

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./backend /code/backend

WORKDIR /code/backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]





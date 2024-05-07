FROM zauberzeug/nicegui:latest

COPY requirements.txt .
COPY ./app /app

RUN python3 -m pip install -r requirements.txt
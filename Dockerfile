FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ARG KENTAVRA_VERSION="dev"
RUN sed -i "s/^VERSION=\".*\"/VERSION=\"${KENTAVRA_VERSION}\"/" kentavra/env

ENV UI_PORT=8000
CMD ["python", "ui/app.py"]

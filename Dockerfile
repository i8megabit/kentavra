FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV UI_PORT=8000
CMD ["python", "ui/app.py"]

FROM golang:1.20 AS builder
WORKDIR /src
COPY cmd/ cmd/
COPY go.mod .
RUN go build -o /kentavra-go cmd/kentavra/main.go

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
COPY --from=builder /kentavra-go /usr/local/bin/kentavra-go

ARG KENTAVRA_VERSION="dev"
RUN sed -i "s/^VERSION=\".*\"/VERSION=\"${KENTAVRA_VERSION}\"/" kentavra/env

ENV UI_PORT=8000
CMD ["python", "ui/app.py"]

FROM python:3.12.3-slim-bookworm AS python-base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

FROM python-base AS builder

WORKDIR /opt/app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

FROM python-base AS final

WORKDIR /opt/app

COPY ./src /opt/app/src 

EXPOSE 80

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]

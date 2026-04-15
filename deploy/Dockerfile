FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends\
    build-essential \
    curl \
    gettext \
    && rm -rf /var/lib/apt/lists/*

#Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -\
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

RUN poetry config virtualenvs.create false
RUN poetry self add poetry-plugin-export

#Зависимости

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt --without-hashes -o requirements.txt\
    && pip install --no-cache-dir -r requirements.txt\
    && rm requirements.txt

COPY .. .



LABEL authors="dima"


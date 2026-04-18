FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends\
    build-essential \
    curl \
    gettext \
    make\
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

COPY . .

ENV DJANGO_SETTINGS_MODULE=config.settings.base

LABEL authors="dima"
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


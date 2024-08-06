FROM python:3

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.2 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    build-essential \
    gettext \
    libpq-dev \
    wget \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    && pip install "poetry-core==1.4.0" "poetry==$POETRY_VERSION" && poetry --version

WORKDIR /code

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

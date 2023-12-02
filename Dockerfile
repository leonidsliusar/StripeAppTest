FROM python:3.11-alpine

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install poetry


COPY pyproject.toml /src/pyproject.toml
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-dev
RUN poetry update
COPY . /src

CMD python manage.py migrate && \
    python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL && \
    gunicorn app.wsgi:application -c gunicorn_config.py

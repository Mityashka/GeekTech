FROM python:3.10

RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean

RUN pip install poetry

WORKDIR /geektech

COPY geektech .

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

RUN python manage.py collectstatic --noinput

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "geektech.wsgi:application"]

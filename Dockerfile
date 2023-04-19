FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY pyproject.toml pdm.lock /project/
COPY . /project

WORKDIR /project
RUN pdm install --prod --no-lock --no-editable

EXPOSE 8000
STOPSIGNAL SIGINT

RUN SECRET_KEY=secret pdm run python manage.py collectstatic --noinput

CMD ["pdm", "start"]

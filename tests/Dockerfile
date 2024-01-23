FROM python:3.11

WORKDIR /opt/app

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_ROOT_USER_ACTION=ignore \
  DOCKERIZE_VERSION="v0.7.0" \
  PYTHONDONTWRITEBYTECODE=1


RUN groupadd -r fastapi && useradd -d /opt/app -r -g fastapi fastapi \
    && chown fastapi:fastapi -R /opt/app/


COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

USER fastapi

ENTRYPOINT ["sh", "/opt/app/docker-entrypoint.sh"]

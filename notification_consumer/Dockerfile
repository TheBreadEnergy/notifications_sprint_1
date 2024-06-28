FROM python:3.12.2
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_ROOT_USER_ACTION=ignore \
  DOCKERIZE_VERSION="v0.7.0"

WORKDIR /opt/app


RUN groupadd -r django && useradd -d /opt/app -r -g django django \
    && chown django:django -R /opt/app/

COPY  requirements.txt requirements.txt
COPY  docker-entrypoint.sh docker-entrypoint.sh

RUN  python -m pip install --upgrade pip \
     && pip install --no-cache-dir -r  requirements.txt \
     && chmod +x docker-entrypoint.sh

COPY . .

USER django

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
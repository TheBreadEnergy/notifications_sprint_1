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

# Create dir for storing log files
RUN mkdir -p /opt/logs/ && chown fastapi:fastapi -R /opt/logs/


COPY requirements.txt requirements.txt

COPY docker-entrypoint.sh docker-entrypoint.sh

RUN apt-get update  \
    && apt-get -y install netcat-traditional \
    curl && python -m pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

USER fastapi

ENTRYPOINT ["/opt/app/docker-entrypoint.sh"]

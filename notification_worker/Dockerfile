FROM python:3.12

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_ROOT_USER_ACTION=ignore \
  DOCKERIZE_VERSION="v0.7.0"

WORKDIR /opt/app

RUN apt-get update  \
    && apt-get -y install netcat-traditional \
    curl 

RUN groupadd -r worker && useradd -d /opt/app -r -g worker worker \
    && chown worker:worker -R /opt/app/

COPY  requirements.txt requirements.txt
COPY  entrypoint.sh entrypoint.sh


RUN  python -m pip install --upgrade pip \
     && pip install --no-cache-dir -r  requirements.txt \
     && chmod +x entrypoint.sh


COPY . .


USER worker

ENTRYPOINT ["sh", "./entrypoint.sh"]
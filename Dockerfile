FROM python:3.9.13-alpine3.16
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT_MODE='docker'
WORKDIR /app
COPY . .
RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                mariadb-dev \
                python3-dev \
                postgresql-dev \
        ;

RUN pip install -r requirements.txt
CMD [ "python", "manage.py", "runserver"]

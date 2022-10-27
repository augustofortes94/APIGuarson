FROM 3.9.15-alpine3.16
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
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
CMD [ "gunicorn", "ProyectoAPI.wsgi"]
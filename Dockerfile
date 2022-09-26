FROM python:3.9-alpine3.16

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "manage.py", "runserver"]

# Notes of project

COMMAND update all Packages:
pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}
pip freeze > requirements.txt


DOCKER:
run command "docker-compose up"

Database= host:'host.docker.internal' will bind to db on the pc host. If you want use a db in the container, may be used 'localhost'.

If you use 0.0.0.0: the project will be accessible from the pc host, but if you don't specifie the address or write 127.0.0.1,
the project only will accessible from the inside of the container.
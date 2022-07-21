# APIGuarson

This app/api is a complement to a telegram bot whose main objective is to provide the combinations of weapon accessories for the game Call of Duty: Warzone.
Recreational only.

*** 2 WAYS TO START PROJECT ***

    START PROJECT WITH DOCKER:
        1. Create a file named ".env" at main folder with the same format described below
        2. Run command 'docker-compose up --build'
        3. (Optional) Run 'docker-compose logs -f' to see logs


    START PROJECT AT LOCALHOST:
        1. Install python on the computer in version > 3.9.5 (set the environment variable path as corresponse)
        2. (optional) Create virtual environment (./[Name of virtual environment]/Scripts/activate)
        3. Install all requirements (pip install -r requirements.txt)
        4. Install PostgreSQL and create a database named "apiguarson" with pgAdmin and restore a backup from the file "backup"
        5. Create a file named ".env" at folder 'ProyectoAPI' with the same format described below
        6. At folder "/APIGuarson" run "python manage.py makemigrations", "python manage.py migrate" and finally "python manage.py runserver"
        7. Open app at localhost:8000/





*** .env format ***
SECRET_KEY=
DATABASE_HOST=
DATABASE_PORT=
DATABASE_USER=
DATABASE_PSW=
DATABASE_NAME=
DEBUG_MODE=
ALLOWED_HOSTS=


COMMAND update all Packages:
pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}


# Note
If the app on debug = False is giving 'Error 500', run the command collectstatic.
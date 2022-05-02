# APIGuarson

This app/api is a complement to a telegram bot whose main objective is to provide the combinations of weapon accessories for the game Call of Duty: Warzone.
Recreational only.

START PROJECT AT LOCALHOST:

1. Install python on the computer in version > 3.9.5 (set the environment variable path as corresponse)
2. (optional) Create virtual environment (./[Name of virtual environment]/Scripts/activate)
3. Install all requirements (pip install -r requirements.txt)
4. Install PostgreSQL and create a database named "apiguarson" with pgAdmin and restore a backup from the file "backup"
5. At folder "/APIGuarson" run "python manage.py makemigrations", "python manage.py migrate" and finally "python manage.py runserver"
6. Open app at localhost:8000/


COMMAND update all Packages:
pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}
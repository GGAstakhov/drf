
poetry env use python3.11
poetry shell
poetry install
python3 manage.py migrate
exit
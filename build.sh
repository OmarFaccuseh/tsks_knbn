 
# exit on error
set -o errexit

pipenv install --deploy --ignore-pipfile

python manage.py collectstatic --no-input
python manage.py migrate
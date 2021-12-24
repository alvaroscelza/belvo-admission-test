# Belvo Admission Test

Admission Test for Belvo Company

Notes:
- I am only using master branch because I'm the only developer (so this would be an SVN-like repository).

## Installation and running

- Create virtual environment and activate it. Example: `virtualenv venv`
- Enter environment: Example: `venv\Scripts\activate`
- `pip install -r requirements.txt`
- `pre-commit install`
- Create an .env file at project root for storing secrets. File .env-example is provided as a guide of this file's
  content. Make sure you copy your SECRET_KEY there. (You can use
  [Djecrety](https://djecrety.ir/), or any other token generator to generate Settings SECRET_KEY)
- `python manage.py makemigrations`
- `python manage.py migrate`
- Run using `python manage.py runserver`

## Testing

- Run the tests with `python manage.py test`
- Get test coverage with `coverage run --source='.' manage.py test` and then `coverage report --skip-covered`

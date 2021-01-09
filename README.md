# PrivateBlog.co

Setting this up from fresh?
```
poetry install
poetry shell
code . # Select the proper shell from lower left corner

# migrating and running the server
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```
- Create the appropriate site for the url (dev/prod)
- Create the appropriate social application for twitter
    - set up until `accounts/twitter/login` works properly
    - set up the social application at `admin/socialaccount/socialapp`
    - docs: https://django-allauth.readthedocs.io/en/latest/providers.html#twitter
    - need more debugging? https://github.com/pennersr/django-allauth/pull/2175
    - make sure the correct Consumer Key and Consumer Secret Key is inputted
- ???
- PROFIT

## Run using gunicorn
```
gunicorn --workers=4 privateblog.wsgi
```

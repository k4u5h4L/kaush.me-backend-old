# kaush.me (old) backend

Open-sourcing the backend of my old portfolio/blog site since it's not in production anymore.

## Features:

- Fully functional REST API with JWT support for Authentication and Authorisation, made using Django Rest Framework.
- File-system based route caching to minimise calls to the database. Customizable cache timeout.
- Inbuilt Django admin panel with a custom installable and customizable theme.
- Google ReCaptcha v2 for admin login page for added security against bots.
- Admin page honeypot to log access attempts to the database. Capture credentials and IP addresses.
- Route based rate limiting for protection against DOS-based attacks.
- User region tracking built into the Django admin panel.
- Custom error-not-found route.

## To run:

- Clone this repo.
- Create a python virtual environment, and install dependencies in `requirements.txt`.

```bash
pip install -r requirements.txt
```

- Make a file called `config.json` in the `server/` dir and add in required API keys and secret keys. Follow the JSON structure given in `server/config_sample.json`.
- Run database migrations and create a superuser.

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

- Now run the server

```bash
python manage.py runserver
```

Your server should be running on port 8000. Visit [localhost:8000](http://localhost:8000/) on your system to see. (Visit the routes present in the `api/urls.py`. You can make your own routes too.)

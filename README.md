<div align="center">

# Signs for Trucks

![Python version](https://img.shields.io/badge/Python-3.12.0-4c566a?logo=python&&longCache=true&logoColor=white&colorB=pink&style=flat-square&colorA=4c566a) ![Django version](https://img.shields.io/badge/Django-5.2.8-4c566a?logo=django&&longCache=truelogoColor=white&colorB=pink&style=flat-square&colorA=4c566a) ![Django-RestFramework](https://img.shields.io/badge/Django_Rest_Framework-3.16.1-red.svg?longCache=true&style=flat-square&logo=django&logoColor=white&colorA=4c566a&colorB=pink) ![Docker](https://img.shields.io/badge/Docker-ready-4c566a?logo=docker&longCache=true&logoColor=white&colorB=pink&style=flat-square&colorA=4c566a)

![Truck Signs](./src/screenshots/Truck_Signs_logo.png)

__Signs for Trucks__ is an online store to buy pre-designed vinyls with custom lines of letters (often call truck letterings).
The store also allows clients to upload their own designs and to customize them on the website as well.

</div>

## Table of Contents

- [Signs for Trucks](#signs-for-trucks)
  - [Table of Contents](#table-of-contents)
  - [About this Repository](#about-this-repository)
  - [Quickstart](#quickstart)
    - [Prerequisites](#prerequisites)
    - [Quick Start (local Python environment)](#quick-start-local-python-environment)
    - [How to Build the Image](#how-to-build-the-image)
  - [Usage](#usage)
    - [Environment Configuration](#environment-configuration)
    - [Building the Container Image](#building-the-container-image)
    - [Running with Docker Compose (recommended)](#running-with-docker-compose-recommended)
    - [Running with `docker run`](#running-with-docker-run)
    - [Switching Between SQLite and PostgreSQL](#switching-between-sqlite-and-postgresql)
    - [Settings](#settings)
    - [Models](#models)
    - [Brief Explanation of the Views](#brief-explanation-of-the-views)
  - [Screenshots of the Django Backend Admin Panel](#screenshots-of-the-django-backend-admin-panel)
    - [Mobile View](#mobile-view)
    - [Desktop View](#desktop-view)
  - [Additional Information](#additional-information)
    - [Postgresql Database](#postgresql-database)
    - [Docker](#docker)
    - [Django and DRF](#django-and-drf)
    - [Testing and CI](#testing-and-ci)
    - [Miscellaneous](#miscellaneous)

## About this Repository

This repository contains the **backend API** for Signs for Trucks, a Django + Django REST Framework
application that powers an online store for custom truck vinyl letterings.

The main contents of the repository are:

- **`src/tsa_app`** – the Django project configuration (settings, URLs, WSGI entrypoint).
- **`src/tsa_products`** – the Django app containing the store's models, serializers and API views
  (categories, products, lettering items, orders, customer image uploads, ...).
- **`Dockerfile`**, **`docker-compose.yml`** and **`entrypoint.sh`** – everything needed to build and
  run the API together with a PostgreSQL database as containers.
- **`docs/`** – supplementary documentation (e.g. linting/testing setup).
- **`.github/workflows`** – CI pipelines that run linting and tests on every push/PR.

The purpose of the repository is to provide a self-contained, easily deployable API that:

- serves the product catalog (categories, products and their lettering/customization options) to a
  frontend client,
- lets customers upload their own designs and turn them into custom products,
- handles order creation, and
- exposes a Django Admin panel for store operators to manage products, categories and orders.

## Quickstart

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and the [Docker Compose plugin](https://docs.docker.com/compose/install/) (recommended way to run the project)
- [Python 3.12.x](https://www.python.org/downloads/release/python-3120/) (only needed if you want to run the app without Docker)
- [Git](https://git-scm.com/downloads)

### Quick Start (local Python environment)

If you just want to run the API directly on your machine (without Docker), use SQLite in dev mode:

```bash
# 1. Clone the repo
git clone git@github.com:Developer-Akademie-DevSecOpsKurs/truck-signs-api.git
cd truck-signs-api

# 2. Copy the example environment file
cp example.env .env

# 3. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Apply database migrations (uses SQLite by default, see "Switching Between SQLite and PostgreSQL")
python src/manage.py makemigrations
python src/manage.py migrate

# 6. Collect static files
python src/manage.py collectstatic

# 7. Start the development server
python src/manage.py runserver
```

The app is now running at [localhost:8000](http://localhost:8000).

### How to Build the Image

The project ships with a `Dockerfile` that builds a self-contained image running the API with
`gunicorn`. To build the image locally, run the following from the project root (where the
`Dockerfile` is located):

```bash
docker build -t tsa-local .
```

This produces a local image tagged `tsa-local`, which is the image referenced by
`docker-compose.yml`. See [Usage](#usage) for how to configure and run the resulting image,
either via Docker Compose or with a plain `docker run`.

## Usage

This section describes the full, containerized setup in detail, including how to configure and
adjust it to get different results (e.g. switching database backends, changing exposed ports, or
plugging in your own credentials).

### Environment Configuration

All runtime configuration is provided via environment variables, typically stored in a `.env` file
in the project root (used by both the plain Python setup and Docker). Start by copying the example
file:

```bash
cp example.env .env
```

Then edit `.env` and fill in the values that apply to your setup. The following variables are read
by the application (see `src/tsa_app/settings.py`) and by `docker-compose.yml`:

| Variable | Purpose | Notes |
| --- | --- | --- |
| `MODE` | `dev` uses SQLite, `prod` uses PostgreSQL | unset/`dev` needs no DB variables |
| `DEBUG` / `DEBUG_ENABLED` | Enables Django debug mode | keep `False`/unset in production |
| `SECRET_KEY` | Django cryptographic secret key | generate a new one, see [Additional Information](#django-and-drf) |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames | e.g. `localhost,127.0.0.1,tsa-web` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins | e.g. the URL of your frontend |
| `DB_HOST` / `DB_PORT` | Hostname/port of the PostgreSQL server | `tsa_db` / `5432` when using Docker Compose |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | PostgreSQL database name and credentials | used both by the `db` container and by Django |
| `CLOUD_NAME` / `CLOUD_API_KEY` / `CLOUD_API_SECRET` | Cloudinary credentials for media storage | leave empty to fall back to local file storage |
| `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | Credentials for sending order emails | any placeholder works while email sending is disabled |
| `DJANGO_SUPERUSER_USERNAME` / `DJANGO_SUPERUSER_EMAIL` / `DJANGO_SUPERUSER_PASSWORD` | Credentials for the admin user auto-created by `entrypoint.sh` | used only inside the Docker container |

Changing these values is the primary way to adapt the deployment: for example, set `MODE=prod` and
fill in the `POSTGRES_*`/`DB_*` variables to run against PostgreSQL, provide `CLOUD_*` variables to
store uploaded media on Cloudinary instead of the local filesystem, or adjust `ALLOWED_HOSTS`/
`CORS_ALLOWED_ORIGINS` to match the domains you deploy to.

### Building the Container Image

```bash
docker build -t tsa-local .
```

- `-t tsa-local` tags the built image as `tsa-local`. This name is what `docker-compose.yml`
  expects for the `backend` service — if you rename the tag, update the `image:` field in
  `docker-compose.yml` (or the `tsa-local` reference in the `docker run` example below) accordingly.
- To rebuild after changing dependencies (`requirements.txt`) or source code, simply re-run the same
  command; Docker will use its build cache for unchanged layers.

### Running with Docker Compose (recommended)

Once the image is built and `.env` is configured, start the full stack (API + PostgreSQL) with:

```bash
docker compose up
```

This starts two containers, as defined in `docker-compose.yml`:

- **`tsa_db`** – a PostgreSQL 18.4 instance, configured from `POSTGRES_DB`/`POSTGRES_USER`/
  `POSTGRES_PASSWORD` in `.env`, exposed on host port `5432` and persisted in the `postgres_data`
  volume.
- **`tsa_backend`** – the Django API built from the `tsa-local` image, exposed on host port `8020`
  (mapped to container port `8000`), waiting for the database to become healthy before running
  migrations, collecting static files, creating the superuser and starting `gunicorn`
  (see `entrypoint.sh`).

The API is then reachable at [localhost:8020](http://localhost:8020), and the admin panel at
[localhost:8020/admin](http://localhost:8020/admin).

To change the exposed host ports, edit the `ports:` sections in `docker-compose.yml` (e.g. change
`'8020:8000'` to `'<your_port>:8000'`). To run in the background, append `-d`; to rebuild the image
as part of the same command, use `docker compose up --build`.

### Running with `docker run`

If you don't want to use Docker Compose, you can run the same setup with plain `docker run`
commands. Replace every `<placeholder>` below with the corresponding value from your `.env` file.

```bash
# 1. Create a shared network so the containers can reach each other
docker network create tsa-network

# 2. Start PostgreSQL
docker run -d \
  --name tsa_db \
  --network tsa-network \
  -e POSTGRES_DB=<postgres_db> \
  -e POSTGRES_USER=<postgres_user> \
  -e POSTGRES_PASSWORD=<postgres_password> \
  -v postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18.4

# 3. Build the backend image (see "Building the Container Image") and run it
docker run -d \
  --name tsa_backend \
  --network tsa-network \
  -e MODE=prod \
  -e SECRET_KEY=<django_secret_key> \
  -e DB_HOST=tsa_db \
  -e DB_PORT=5432 \
  -e POSTGRES_DB=<postgres_db> \
  -e POSTGRES_USER=<postgres_user> \
  -e POSTGRES_PASSWORD=<postgres_password> \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  -e DJANGO_SUPERUSER_USERNAME=<admin_username> \
  -e DJANGO_SUPERUSER_EMAIL=<admin_email> \
  -e DJANGO_SUPERUSER_PASSWORD=<admin_password> \
  -v "$(pwd)/src/staticfiles:/app/src/staticfiles" \
  -v "$(pwd)/src/media:/app/src/media" \
  -p 8020:8000 \
  tsa-local
```

Instead of listing every `-e` flag individually, you can pass `--env-file .env` to reuse the values
already configured in your `.env` file. The API will then be reachable at
[localhost:8020](http://localhost:8020), same as with Docker Compose.

### Switching Between SQLite and PostgreSQL

The database backend is controlled entirely by the `MODE` environment variable
(see `src/tsa_app/settings.py`):

- `MODE` unset or `MODE=dev` → SQLite database file at `src/db.sqlite3`; no DB-related env vars
  required. This is the default for the plain Python [Quick Start](#quick-start-local-python-environment).
- `MODE=prod` → PostgreSQL, using `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `DB_HOST` and
  `DB_PORT` from `.env`. This is what the Docker setup uses by default.

To point the app at a different PostgreSQL server (e.g. a managed cloud database instead of the
`tsa_db` container), set `MODE=prod` and update `DB_HOST`/`DB_PORT`/`POSTGRES_*` accordingly — no
code changes are required.

### Settings

The `settings.py` file inside the `src/tsa_app` folder contains the Django settings configuration
for the application, and reads all of its configurable values from the environment variables
described in [Environment Configuration](#environment-configuration).

### Models

Most of the models do what can be inferred from their name. The following notes clarify the
purpose of some of the models:
- __Category Model:__ The category of the vinyls in the store. It contains the title of the category as well as the basic properties shared among products that belong to a same category. For example, _Truck Logo_ is a category for all vinyls that has a logo of a truck plus some lines of letterings (note that the vinyls are instances of the model _Product_). Another category is _Fire Extinguisher_, that is for all vinyls that has a logo of a fire extinguisher.
- __Lettering Item Category:__ This is the category of the lettering, for example: _Company Name_, _VIM NUMBER_, ... Each has a different pricing.
- __Lettering Item Variations:__ This contains a foreign key to the __Lettering Item Category__ and the text added by the client.
- __Product Variation:__ This model has the original product as a foreign key, plus the lettering lines (instances of the __Lettering Item Variations__ model) added by the client.

### Brief Explanation of the Views

Most of the views are CBV imported from _rest_framework.generics_, and they allow the backend api to do the basic CRUD operations expected, and so they inherit from the _ListAPIView_, _CreateAPIView_, _RetrieveAPIView_, ..., and so on.

The behavior of some of the views had to be modified to address functionalities such as creation of order and payment, as in this case, for example, both functionalities are implemented in the same view, and so a _GenericAPIView_ was the view from which it inherits. Another example of this is the _UploadCustomerImage_ View that takes the vinyl template uploaded by the clients and creates a new product based on it.

> [!NOTE]
> To create Truck vinyls with Truck logos in them, first create the __Category__ Truck Sign,
> and then the __Product__ (can have any name). This is to make sure the frontend retrieves
> the Truck vinyls for display in the Product Grid as it only fetches the products of the
> category Truck Sign.

---

## Screenshots of the Django Backend Admin Panel

### Mobile View

<div style="padding: 0 5rem; width: 100%;  display: flex; gap: 5rem; justify-content: center; flex-wrap: wrap;">

![alt text](./src/screenshots/Admin_Panel_View_Mobile.png)

![alt text](./src/screenshots/Admin_Panel_View_Mobile_2.png)

![alt text](./src/screenshots/Admin_Panel_View_Mobile_3.png)

</div>

### Desktop View


<div style="padding: 0 5rem; width: 100%; display: flex; flex-direction: column; gap: 2rem; align-items: center; justify-content: center;">

![alt text](./src/screenshots/Admin_Panel_View.png)

![alt text](./src/screenshots/Admin_Panel_View_2.png)

![alt text](./src/screenshots/Admin_Panel_View_3.png)

</div>

## Additional Information

### Postgresql Database

- Setup Database: [Digital Ocean Link for Django Deployment on VPS](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)

### Docker

- [Docker Official Documentation](https://docs.docker.com/)
- Dockerizing Django, PostgreSQL, guinicorn, and Nginx:
    - Github repo of sunilale0: [Link](https://github.com/sunilale0/django-postgresql-gunicorn-nginx-dockerized/blob/master/README.md#nginx)
    - Michael Herman article on testdriven.io: [Link](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)

### Django and DRF

- [Django Official Documentation](https://docs.djangoproject.com/en/5.2/)
- Generate a new secret key: [Stackoverflow Link](https://stackoverflow.com/questions/41298963/is-there-a-function-for-generating-settings-secret-key-in-django)
- Modify the Django Admin:
    - Small modifications (add searching, columns, ...): [Link](https://realpython.com/customize-django-admin-python/)
    - Modify Templates and css: [Link from Medium](https://medium.com/@brianmayrose/django-step-9-180d04a4152c)
- [Django Rest Framework Official Documentation](https://www.django-rest-framework.org/)
- More about Nested Serializers: [Stackoverflow Link](https://stackoverflow.com/questions/51182823/django-rest-framework-nested-serializers)
- More about GenericViews: [Testdriver.io Link](https://testdriven.io/blog/drf-views-part-2/)

### Testing and CI

- Linting (`flake8`, `isort`, `black`) and the Django test suite are documented in [docs/testing.md](./docs/testing.md).
- CI workflows live in [.github/workflows](./.github/workflows) and run on every push/PR.

### Miscellaneous

- Create Virual Environment with Virtualenv and Virtualenvwrapper: [Link](https://docs.python-guide.org/dev/virtualenvs/)
- [Configure CORS](https://www.stackhawk.com/blog/django-cors-guide/)
- [Setup Django with Cloudinary](https://cloudinary.com/documentation/django_integration)

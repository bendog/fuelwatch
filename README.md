# Fuel Watch Rest/GraphQL api example

Proof of concept for a dynamic backend for Fuel Watch scraping.

## Django+Graphene app

todo:

- better filtering
- better sorting

### setup a new database

    cd fuelapp
    ./manage.py migrate
    ./manage.py runserver

then browse to <http://127.0.0.1:8000/update> to populate the database

### run an existing app

    cd fuelapp
    ./manage.py runserver

then browse to <http://127.0.0.1:8000/>

## Flask app

todo:

- pretty much everything

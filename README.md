# Fuel Watch Rest/GraphQL api example

Proof of concept for a dynamic backend for Fuel Watch scraping.

## Django + Graphene + Django-Rest-Framework app

todo:

- Django Rest filter for date valid today
- Django GraphQL filter for date valid today

### setup a new database

    cd fuelapp
    ./manage.py migrate
    ./manage.py runserver

then browse to <http://127.0.0.1:8000/update> to populate the database

### run an existing app

    cd fuelapp
    ./manage.py runserver

then browse to <http://127.0.0.1:8000/graphql> for graphql interface
or browse to  <http://127.0.0.1:8000/rest/> for django rest framework interface

### Django Rest Framework example queries

- price list for a collection of suburbs <http://localhost:8000/rest/price/?location__suburb__in=SOUTH+PERTH%2CCOMO%2CMANNING%2CKENSINGTON&ordering=price>
- price list for a brand <http://localhost:8000/rest/price/?location__brand__istartswith=BP&ordering=price>
- price list for a date <http://localhost:8000/rest/price/?date__gte=2019-05-28&ordering=price>
- location list ordered by suburb with prices >= a date <http://localhost:8000/rest/location/?prices__date__gte=2019-05-28&ordering=suburb>

### Django Graphene graphql example queries

Search for all fuel in a suburb

```graphql
{
  allLocations(suburb: "PERTH") {
    edges {
      node {
        id
        brand
        address
        prices {
          edges {
            node {
              price
            }
          }
        }
      }
    }
  }
}
```

Search for all Caltex, Shell and BP, sorting by Price and return first 50

```graphql
{
  allLocations(orderBy:"prices__price", first:50, brand_In:"Caltex,Shell,BP") {
    edges {
      node {
        id
        brand
        address
        prices {
          edges {
            node {
              price
            }
          }
        }
      }
    }
  }
}
```


## Flask app

todo:

- pretty much everything

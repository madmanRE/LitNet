# LitNet - all the books in your hands!

---

TODO:
* ~~Backend~~
  * ~~Create FastAPI app~~
  * ~~Connect DB~~
  * ~~Make CRUD~~
  * ~~Make registration~~
  * ~~Create tests~~
* Frontend
  * Create Vue js app
  * Create fetch query for Google Books API
  * ...
* ~~Deploy~~
  * ~~Run app into Docker~~

**LitNet** - is a ***CRUD*** web-app. 

Users must be registered to add books to their collection, read information, update, and delete them.


## Backend
___  

### Routers

| METHOD   | ROUTE                             | FUNCTIONALITY                 |ACCESS|
|----------|-----------------------------------|-------------------------------| ------------ |
| *POST*   | ```/auth/signup/```               | _Register new user_           |_All users_|
| *POST*   | ```/auth/login/```                | _Login user_                  |_All users_|
| *GET*    | ```/auth/refresh/```              | _Refresh access token_        |_All users_|
| *GET*    | ```/books/```                     | _Get all books of the user_   |_Authenticated users_|
| *GET*    | ```/books/{book_title}/```        | _Get a book by title_         |_Authenticated users_|
| *POST*   | ```/books/add/```                 | _Add a book to collections_   |_Authenticated users_|
| *PATCH*  | ```/books/update/{boot_title}/``` | _Update a book in collection_ |_Authenticated users_|
| *DELETE* | ```/books/delete/```              | _Delete a book in collection_ |_Authenticated users_|
| *GET*    | ```/docs/```                      | _View API documentation_      |_All users_|

### Backend structure

```
.
└── backend
    ├── auth_routers.py
    ├── book_routers.py
    ├── database.py
    ├── init_db.py
    ├── main.py
    ├── models.py
    ├── schemas.py
    └── tests.py
```

### Installation backend app

* Install Postgresql
  * [pgAdmin](https://www.pgadmin.org/download/) helps to manage db with UI interface
* Install Python
* Git clone the project with  git clone https://github.com/madmanRE/LitNet.git
* Create your virtualenv with Pipenv or virtualenv and activate it
* Install the requirements with pip install -r requirements.txt
* Set Up your PostgreSQL database and set its URI in your database.py
  `engine=create_engine('postgresql://postgres:<username>:<password>@localhost/<db_name>',echo=True)`
* Create your database by running python init_db.py
* Finally run the API `uvicorn main:app`


#### Run it in Docker

* Install Docker
  * [Docker Desktop](https://www.docker.com/products/docker-desktop/) helps to manage containers with UI interface
* Build app image with the command `docker build -t <image_name> . `
* Run it into container `docker run -d --name <container_name> -p 80:80 <image_name> `
* **Warning**: now dependencies have unresolved conflict:
  * *fastapi 0.99.1 depends on pydantic!=1.8, !=1.8.1, <2.0.0 and >=1.7.4*
  * *pydantic-extra-types 2.0.0 depends on pydantic>=2.0b3*
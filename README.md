# LitNet - all the books in your hands!

---

TODO:
* Backend
  * ~~Create FastAPI app~~
  * ~~Connect DB~~
  * ~~Make CRUD~~
  * ~~Make registration~~
  * Create tests
* Frontend
  * Create Vue js app
  * ...
* Deploy
  * Run app into Docker

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

### Structure

```
.
└── let_net
    ├── auth_routers.py
    ├── book_routers.py
    ├── database.py
    ├── init_db.py
    ├── main.py
    ├── models.py
    ├── schemas.py
    └── tests.py
```





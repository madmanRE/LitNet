# LitNet - все книги мира в твоем кармане!

---

**LitNet** - это *CRUD* веб-приложение, посвященное книгам. 

Пользователи смогут добавлять собственные книги и отмечать статус:
* Желаю
* Уже в коллекции
* Прочитано
* Рекомендую

Соответственно, у пользователей будет возможность просматривать, удалять, добавлять и изменять книги.

Также пользователь сможет получить дополнительную информацию из Google Books Api.

---

## Используемые технологии

* Backend - FastAPI
* DataBase - PostgreSQL
* Container - Docker
* Version Control - Git

---

## Создание проекта по шагам

### Инициализация проекта

* Создал директорию
* Внутри подключил и активировал виртуальное окружение
>`python -m venv env`
* Инициализировал контроль версий Git
* Добавил .gitignore
* Установил FastAPi 
>`pip install "fastapi[all]"`

### Разработка маршрутов

| METHOD | ROUTE                           | FUNCTIONALITY                                 |ACCESS|
| ------- |---------------------------------|-----------------------------------------------| ------------ |
| *POST* | ```/auth/signup/```             | _Register new user_                           |_All users_|
| *POST* | ```/auth/login/```              | _Login user_                                  |_All users_|
| *GET* | ```/books/```                   | _Get all books of the user_                   |_Authenticated users_|
| *GET* | ```/books/{book_title}/```      | _Get a book_                                  |_Authenticated users_|
| *GET* | ```/books/like/{book_title}/``` | _Get a list of similar books_                 |_Authenticated users_|
| *GET* | ```/books/unloading/```         | _Get all the books of the user in csv / json_ |_Authenticated users_|
| *POST* | ```/books/add/```               | _Add a book to collections_                   |_Authenticated users_|
| *PUT* | ```/books/{boot_title}/```      | _Update a book in collection_                 |_Authenticated users_|
| *DELETE* | ```/books/delete/{book_id}/```  | _Delete a book in collection_                 |_Authenticated users_|
| *GET* | ```/docs/```                    | _View API documentation_                      |_All users_|

### Разработка модели данных

Расширил структуру проекта

```
.
└── let_net
    ├── auth_routers.py
    ├── book_routers.py
    ├── database.py
    ├── main.py
    ├── models.py
    └── schemas.py
```

Затем реализовал модели типов (schemas):

```
class Book(BaseModel):
    id: int
    title: str
    description: Optional[str]
    author: Author
    genre: Optional[Genre]
    status: Optional[str] = "WISHING"
```

### Подключение к базе данных




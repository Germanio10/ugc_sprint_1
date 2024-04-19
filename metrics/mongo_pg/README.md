# Тестирование производительности Mongo и Postgres

Пользователей: 10000
Фильмов: 1000
Лайков: 10000000

## Результаты
## -----------Postgres------------
Вставка в таблицу лайков...
Количество записей: 10000000
Время работы функции 138763.05 мс.

Получение id пользователя, id фильма..
Время работы функции 1.41 мс.

Получение списка фильмов, понравившихся пользователю..
Время работы функции 421.87 мс.
Результат:  518

Получение количества лайков фильма...
Время работы функции 301.53 мс.
Результат:  5059

Получение рейтинга фильма...
Время работы функции 302.54 мс.
Результат: 0.51

Добавление лайка...
Время работы функции 1.11 мс.

Получение лайка...
Время работы функции 290.99 мс.

## -------------Mongo-------------
Вставка в таблицу лайков...
Количество записей: 10000000
Время работы функции 463316.37 мс.

Получение id пользователя, id фильма..
Время работы функции 1.87 мс.

Получение списка фильмов, понравившихся пользователю..
Время работы функции 4187.89 мс.
Результат:  518

Получение количества лайков фильма...
Время работы функции 3302.15 мс.
Результат:  5059

Получение рейтинга фильма...
Время работы функции 3151.96 мс.
Результат: 0.51

Добавление лайка...
Время работы функции 1.04 мс.

Получение лайка...
Время работы функции 3966.04 мс.

## Запуск теста
1. Скопировать настройки переменных окружения из .env.example в .env:
```shell
cp .env.example .env
```

3. Запустить проект:
```shell
docker compose up
```
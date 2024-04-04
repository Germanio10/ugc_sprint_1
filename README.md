## Ссылка на инвайт для ревью:
https://github.com/Germanio10/ugc_sprint_1/invitations

# Сервис сбора пользовательских действий

Сервис, предоставляющий сбор пользовательских действий для онлайн-кинотеатра

### Используемые технологии
Язык: python + FastAPI
Сервер: ASGI(uvicorn)
Хранилище: Clickhouse
Брокер: Apache Kafka
Контейнеризация: Docker
Тестирование: Pytest

## Установка и запуск
1. Склонировать данный репозиторий c API:
```shell
git clone git@github.com:Germanio10/ugc_sprint_1.git
```

2. Скопировать настройки переменных окружения из .env.example в .env:
```shell
cp .env.example .env
```

3. Запустить проект:
```shell
docker compose up
```

5. Тесты автоматически запускаются после запуска проекта

Для отдельного запуска тестов необходимо ввести:
```shell
docker-compose up tests
```
## Переменные окружения

| Variable              | Explanation                                         | Example                                                       |
|-----------------------|-----------------------------------------------------|---------------------------------------------------------------|
| `KAFKA_HOSTS`         | Kafka Hostnames                                     | `kafka-0:9092,kafka-1:9092,kafka-2:9092`                      |
| `TOPICS`              | Kafk topics                                         | `["messages"]`                                                |
| `NUM_PARTITIONS`      | Number of partitions                                | `3`                                                           |
| `REPLICATION_FACTOR`  | Replication factor                                  | `3`                                                           |
| `GROUP_ID`            | Kafka group id                                      | `etl_kafka_clickhouse`                                        |
| `CLICKHOUSE_MAIN_HOST`| Clickhouse hostname                                 | `clickhouse-node1`                                            | 
| `CLICKHOUSE_MAIN_PORT`| Clickhouse port                                     | `9000`                                                        |
| `CLICKHOUSE_MULTIPLE_HOSTS`| Clickhouse hostnames                           | `clickhouse-node2, clickhouse-node3, clickhouse-node4`        |
| `FILMS_API_BASE_URL`  | Films api url                                       | `http://fastapi_nginx:81`                                     |

## OpenAPI
Для проверки работоспособности проекта используется Swagger. 
Запускаем проект и по `http://localhost/api/openapi` переходим на Swagger. Здесь можно проверить работу ендпоинтов

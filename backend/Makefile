DC = docker compose
EXEC = docker exec -it
LOGS = docker logs

APP_FILE = docker_compose\app.yaml
STORAGES_FILE = docker_compose\storages.yaml

APP_CONTAINER = irrigation-system-app
DB_CONTAINER = irrigation-system-db
ENV_FILE = --env-file .env


.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV_FILE} up -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV_FILE} up -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: all
all:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV_FILE} up -d

.PHONY: all-down
all-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} alembic revision --autogenerate

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} alembic upgrade head


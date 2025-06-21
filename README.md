```
 ██╗  ██╗███████╗███╗   ██╗████████╗ █████╗ ██╗   ██╗██████╗  █████╗
 ██║ ██╔╝██╔════╝████╗  ██║╚══██╔══╝██╔══██╗██║   ██║██╔══██╗██╔══██╗
 █████╔╝ █████╗  ██╔██╗ ██║   ██║   ███████║██║   ██║██████╔╝███████║
 ██╔═██╗ ██╔══╝  ██║╚██╗██║   ██║   ██╔══██║╚██╗ ██╔╝██╔══██╗██╔══██║
 ██║  ██╗███████╗██║ ╚████║   ██║   ██║  ██║ ╚████╔╝ ██║  ██║██║  ██║
 ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝
```

# Kentavra

"Кентавра" — это набор утилит на Go для развертывания Akvorado через Docker.
Мы не храним сам Akvorado. Скачайте его отдельно и распакуйте в каталог
`akvorado` рядом с папкой `kentavra`.

## Быстрый старт
1. Установите Docker.
2. Клонируйте этот репозиторий.
3. Скачайте [архив Akvorado](https://github.com/akvorado/akvorado/releases)
   и распакуйте его в папку `akvorado`.
4. Соберите Go-версию и запустите её:
   ```bash
   make build
   ./kentavra-go start
   ```

После запуска веб‑интерфейс будет доступен по порту 8081 на локальной машине.

## Отладка и управление
В папке `kentavra` находится скрипт `run` и файл `env` с настройками.
Основные команды:

```bash
./kentavra/run start       # Запуск сервисов
./kentavra/run stop        # Остановка
./kentavra/run restart     # Перезапуск
./kentavra/run status      # Проверка состояния
./kentavra/run logs        # Просмотр логов
./kentavra/run debug       # Диагностика
./kentavra/run clean       # Полное удаление данных
```

Подробнее о возможностях смотрите в [kentavra/README.md](kentavra/README.md).
Быстрое развёртывание описано в [docs/docker-quickstart.md](docs/docker-quickstart.md).


## Docker образ с UI

Соберите контейнер:

```bash
docker build -t kentavra-ui --build-arg KENTAVRA_VERSION=$(cat kentavra/env | grep '^VERSION=' | cut -d'"' -f2) .
```

Запустите его и откройте `http://localhost:8000`:

```bash
docker run -p 8000:8000 kentavra-ui
```

На странице видно версию и статус сервисов. Там же можно запускать команды
оркестратора в пару кликов. Больше деталей в [docs/architecture.md](docs/architecture.md).

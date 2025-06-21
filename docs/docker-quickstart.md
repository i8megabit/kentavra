# Быстрый запуск в Docker

```bash
# Собрать бинарник
make build

# Собрать образ и запустить
docker build -t kentavra .
docker run --rm -p 8081:8081 kentavra
```

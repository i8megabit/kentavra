# Kentavra v1.2.1

Это скриптовый оркестратор для Akvorado. Он автоматизирует запуск
контейнеров, проверяет зависимости и помогает отладить систему.

## Что нужно
- Linux с Docker и bash
- скачанный архив Akvorado. Разархивируйте его в папку `akvorado`
  рядом с каталогом `kentavra`.

## Основные команды
```bash
./run install     # первичная настройка Akvorado
./run start       # запуск сервисов
./run stop        # остановка
./run restart     # перезапуск
./run status      # текущий статус
./run logs        # логи всех сервисов
./run debug       # простая диагностика
./run clean       # полное удаление контейнеров и данных
```

Есть команды для исправления распространённых проблем:
```bash
./run fix dns
./run fix conntrack
./run fix kafka
./run fix jmx
./run fix clickhouse
```

Для теста можно запустить генерацию NetFlow и sFlow:
```bash
./run test softflowd
./run test tcpdump
```

Смотрите файл `env` для настроек портов и путей.


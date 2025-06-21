```
 ██╗  ██╗███████╗███╗   ██╗████████╗ █████╗ ██╗   ██╗██████╗  █████╗
 ██║ ██╔╝██╔════╝████╗  ██║╚══██╔══╝██╔══██╗██║   ██║██╔══██╗██╔══██╗
 █████╔╝ █████╗  ██╔██╗ ██║   ██║   ███████║██║   ██║██████╔╝███████║
 ██╔═██╗ ██╔══╝  ██║╚██╗██║   ██║   ██╔══██║╚██╗ ██╔╝██╔══██╗██╔══██║
 ██║  ██╗███████╗██║ ╚████║   ██║   ██║  ██║ ╚████╔╝ ██║  ██║██║  ██║
 ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝
```

# Kentavra v2.0.2

Теперь Kentavra написана на Go. CLI заменил прежний bash‑скрипт и
позволяет управлять контейнерами Akvorado.

## Что нужно
- Linux с Docker и bash
- скачанный архив Akvorado. Разархивируйте его в папку `akvorado`
  рядом с каталогом `kentavra`.

## Основные команды
```bash
kentavra-go install    # первичная настройка Akvorado
kentavra-go start      # запуск сервисов
kentavra-go stop       # остановка
kentavra-go restart    # перезапуск
kentavra-go status     # текущий статус
kentavra-go logs       # логи всех сервисов
kentavra-go debug      # простая диагностика
kentavra-go clean      # полное удаление контейнеров и данных
```

Есть команды для исправления распространённых проблем:
```bash
kentavra-go fix dns
kentavra-go fix conntrack
kentavra-go fix kafka
kentavra-go fix jmx
kentavra-go fix clickhouse
```

Для теста можно запустить генерацию NetFlow и sFlow:
```bash
kentavra-go test softflowd
kentavra-go test tcpdump
```

Смотрите файл `env` для настроек портов и путей.


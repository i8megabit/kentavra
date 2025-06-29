# Журнал изменений (Changelog)

Все значимые изменения в проекте будут задокументированы в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/),
и этот проект придерживается [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2025-04-08

### Изменено
- Оптимизирована функция `enable_geoip`: сокращен код и упрощен процесс активации GeoIP
- Улучшена документация по использованию оркестратора Kentavra

### Удалено
- Удалена команда `run fix-clickhouse` и вся связанная с ней логика

## [1.2.0] - 2025-04-08

### Добавлено
- Новая команда `run fix-clickhouse` для исправления проблем с томами ClickHouse
- Улучшена поддержка GeoIP: добавлена команда `run enable-geoip` для включения функциональности

### Изменено
- Переименована команда `disable-geoip` в `enable-geoip` с инвертированной логикой
- GeoIP функциональность теперь отключена по умолчанию (закомментированы базы и отключены компоненты)
- Улучшены инструкции по настройке GeoIP с дополнительной информацией о лицензиях

## [1.1.9] - 2025-04-08

### Добавлено
- Команда `run disable-geoip` для полного отключения GeoIP функциональности

### Изменено
- Улучшена функция `clean_data` для корректного удаления томов ClickHouse с проверкой и удалением блокирующих контейнеров

## [1.1.8] - 2025-04-07

### Изменено
- Обновлена команда `run test`:
  - Добавлена поддержка запуска tcpdump для мониторинга NetFlow/sFlow трафика
  - Добавлена поддержка запуска softflowd для генерации тестовых данных
  - Удалена автоматическая генерация сетевого трафика
  - Добавлена возможность прерывания работы команд по Ctrl+C

## [1.1.7] - 2025-04-07

### Добавлено
- Добавлена поддержка переменных окружения в файле `versions.yml` для гибкой настройки версий компонентов
- Добавлены переменные для сетей в `env.sh`

### Изменено
- Команда `fix dns` теперь только настраивает сеть Docker, без автоматического перезапуска сервисов
- Обновлена логика использования переменных версий из `kentavra/env` в файле `versions.yml`
- Улучшены сообщения для пользователя при работе с сетью Docker
- Удалена функция `update_snmp_config` и связанные с ней вызовы

### Исправлено
- Решена проблема с ошибкой "network akvorado_default declared as external, but could not be found"
- Добавлена проверка существования сети Docker перед запуском контейнеров

## [1.1.6] - 2025-04-07

### Добавлено
- Создана новая функция `update_snmp_config` для отдельной настройки SNMP в конфигурационных файлах
- Улучшена документация по актуальной структуре конфигурации SNMP

### Изменено
- Обновлена структура конфигурации SNMP в соответствии с требованиями Akvorado версии 1.11.3+
- В функции `setup_snmp` добавлен вызов `update_snmp_config` для централизованного управления конфигурацией
- Улучшено форматирование YAML-конфигурации для SNMP и метаданных
- Обновлены комментарии для лучшего понимания назначения каждой секции конфигурации

### Исправлено
- Исправлено расположение секции `securityparameters` внутри секции `communities`
- Добавлено корректное указание портов SNMP для каждого IP-адреса
- Обновлена сеть Docker для SNMP-коммуникаций с 172.18.0.0/16 на 172.20.0.0/16

## [1.1.5] - 2025-04-07

### Исправлено
- Исправлена структура конфигурации в inlet.yaml - удалена некорректная секция providers
- Настройки SNMP переработаны для соответствия документации
- Добавлен параметр default в securityparameters для корректной работы SNMP

## [1.1.4] - 2025-04-07

### Изменено
- Функция `install_akvorado` теперь не скачивает архив quickstart, а использует локальный форк
- Добавлена проверка структуры проекта перед настройкой
- Улучшены сообщения для пользователя о ходе установки

## [1.1.3] - 2025-04-07

### Исправлено
- Улучшена функция `clean_data` для корректного удаления контейнеров Redis и Traefik
- Добавлена обработка для исключения контейнера Portainer из процесса удаления
- Реализована построчная обработка контейнеров вместо массовой для повышения надежности
- Добавлена финальная проверка наличия неудаленных контейнеров и томов
- Улучшены диагностика после выполнения команды `run clean`

## [1.1.2] - 2025-04-07

### Исправлено
- Полностью переработана функция `clean_data` для корректного удаления данных Akvorado
- Добавлена поэтапная остановка контейнеров перед их удалением
- Улучшен поиск контейнеров, связанных с Akvorado (включая префикс "docker-")
- Добавлена построчная обработка удаления каждого тома по отдельности
- Добавлено обнаружение контейнеров, блокирующих конкретный том
- Улучшены сообщения об ошибках с рекомендациями по перезапуску Docker

## [1.1.1] - 2025-04-07

### Исправлено
- Улучшена функция `clean_data` для принудительного удаления всех томов Docker, даже если они используются
- Добавлена проверка блокирующих контейнеров и их принудительное удаление при очистке данных
- Улучшена обработка удаления сети Docker при выполнении команды `run clean`

## [1.1.0] - 2025-04-06

### Добавлено
- Новая функция `fix ports` для автоматического разрешения конфликтов портов
- Автоматическая проверка занятости портов перед запуском сервисов
- Поддержка альтернативных портов для Traefik (8082), Web UI (8083) и NetFlow (9995)

### Изменено
- Улучшена обработка ошибок при запуске сервисов
- Добавлены более информативные сообщения об ошибках при проблемах с портами

### Исправлено
- Исправлена проблема с конфликтом портов при запуске сервисов
- Добавлено автоматическое переназначение портов при обнаружении конфликтов

## [1.0.0] - 2025-04-06

### Добавлено
- Создан оркестратор "Kentavra" для управления Akvorado
- Реализован скрипт `run` для управления всеми аспектами работы Akvorado
- Добавлена команда `disable-demo` для отключения демо-режима и настройки боевого окружения
- Добавлена возможность исправления проблем через команду `fix demo`
- Добавлены проверки ошибок во всех критических функциях оркестратора

### Изменено
- Переименована директория оркестратора с `orchestrator` на `kentavra`
- Изменён ASCII-баннер с "AKVORADO" на "KENTAVRA"
- Цвет баннера изменён с зелёного (GREEN) на голубой (CYAN)
- Скрипты переименованы с `.sh` на прямое название (`run.sh` → `run`)
- Обновлена документация с учётом новой структуры и функциональности
- Улучшена функция `fix_kafka_problem()` для корректной обработки ошибок

### Исправлено
- Исправлена проблема с отключением демо-режима в конфигурации Akvorado
- Исправлены некорректные флаги `-it` в командах Docker, вызывающие ошибки в некоторых окружениях

## Нереализованные задачи / TODO
- Добавить мониторинг производительности сервисов
- Реализовать автоматическое обновление компонентов
- Создать графический интерфейс администратора 
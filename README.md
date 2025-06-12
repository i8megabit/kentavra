# Документация по установке и устранению неполадок Akvorado

## Архитектура v1.2.1

Akvorado - система сбора, обогащения и визуализации сетевых потоков. Основные компоненты:

- **Inlet**: принимает и обрабатывает NetFlow/IPFIX/sFlow данные
- **Orchestrator**: управляет конфигурацией и координирует другие компоненты
- **Console**: веб-интерфейс для визуализации и анализа данных

Данные передаются через Kafka, хранятся в ClickHouse и кэшируются с помощью Redis.

### Структура репозитория
```bash
.
├── akvorado/              # Основной каталог
│   ├── config/            # Конфигурация 
│   │   ├── akvorado.yaml  # Основной конфиг
│   │   ├── inlet.yaml     # Настройки Inlet
│   │   ├── console.yaml   # Настройки Console
│   ├── docker/            # Docker-файлы
│   │   ├── grafana/
│   │       ├── dashboards/
│   ├── orchestrator/      # Entrypoint для кликхауса
│   │   ├── clickhouse/
│   │       ├── data/
├── kentavra/
│   ├── run        # Основной скрипт-оркестратор
│   ├── env        # Переменные окружения
│   ├── check      # Скрипт для дебага
│   ├── README.md  # Документация оркестратора
├── CHANGELOG.md  # Журнал изменений проекта
├── README.md     # Основная документация по Akvorado
```

## Использование оркестратора "Kentavra"

Для упрощения установки и управления Akvorado используется оркестратор "Kentavra", который находится в директории `kentavra/`. Оркестратор предоставляет удобный интерфейс командной строки для всех операций.

Оркестратор Kentavra предоставляет удобный интерфейс для управления Akvorado через скрипт `run`. Вот основные команды:

```
./kentavra/run install           # Установка Akvorado
./kentavra/run start             # Запуск всех сервисов
./kentavra/run stop              # Остановка всех сервисов
./kentavra/run restart           # Перезапуск всех сервисов
./kentavra/run status            # Статус всех сервисов
./kentavra/run clean             # Удаление всех данных
./kentavra/run debug             # Запуск диагностики
./kentavra/run logs [сервис]     # Просмотр логов (без аргументов - все сервисы)
./kentavra/run fix [проблема]    # Исправление проблем (dns, conntrack, clickhouse, jmx, kafka)
./kentavra/run snmp-setup        # Настройка SNMP для мониторинга
./kentavra/run db-query [SQL]    # Выполнение запроса к ClickHouse
./kentavra/run test tcpdump      # Запуск tcpdump для мониторинга трафика NetFlow/sFlow
./kentavra/run test softflowd    # Запуск softflowd для генерации тестовых данных NetFlow
./kentavra/run enable-geoip      # Включение функциональности GeoIP (отключена по умолчанию)
```

> **Важно**: Скрипт автоматически настраивает локальную версию Akvorado без скачивания архивов.
> 
> **Важно**: Рекомендуется отключить демо-режим с помощью команды `./kentavra/run disable-demo`

## Дополнительные возможности оркестратора

### Включение и настройка GeoIP

По умолчанию GeoIP функциональность отключена для уменьшения зависимости от внешних сервисов. Если вам нужно обогащение данных географической информацией, выполните:

```bash
./kentavra/run enable-geoip
```

Команда автоматически настроит:
1. Базы данных GeoIP в конфигурационном файле
2. Активирует соответствующий docker-compose файл в .env
3. Предложит перезапустить оркестратор для применения изменений

При использовании MaxMind GeoIP (вместо IPinfo по умолчанию):
1. Получите бесплатную лицензию на сайте [MaxMind](https://www.maxmind.com/en/geolite2/signup)
2. Укажите ваш ACCOUNT_ID и LICENSE_KEY в .env файле
3. Раскомментируйте строку с docker-compose-maxmind.yml вместо docker-compose-ipinfo.yml
4. Обновите пути к базам данных в config/akvorado.yaml

### Решение типичных проблем

Оркестратор Kentavra включает встроенные средства диагностики и исправления распространенных проблем:

```bash
# Диагностика всей системы
./kentavra/run debug

# Исправление проблем с DNS
./kentavra/run fix dns

# Решение проблем с сетевым подключением
./kentavra/run fix conntrack

# Исправление проблем с Kafka
./kentavra/run fix kafka

# Решение конфликтов JMX портов
./kentavra/run fix jmx

# Исправление проблем с ClickHouse
./kentavra/run fix clickhouse
```

При проблемах с томами Docker (ошибки "volume in use"):
1. Используйте `./kentavra/run clean` для полной очистки данных
2. Если тома всё еще невозможно удалить, перезапустите Docker
3. Используйте `./kentavra/run install` и `./kentavra/run start` для повторной установки

Подробную документацию по оркестратору "Kentavra" см. в [kentavra/README.md](kentavra/README.md).

## Установка Docker

### Установка для Ubuntu 24.04

```bash
# Добавляем официальный репозиторий Docker
apt-get update
apt-get install ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Добавляем репозиторий в источники apt
echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Устанавливаем пакеты Docker
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Установка Portainer (опционально)
```bash
docker volume create portainer_data
docker run -d -p 9000:9000 -p 8000:8000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
```

## Установка Akvorado (ручной способ)

> **Примечание**: Рекомендуется использовать оркестратор для установки (`./kentavra/run install`). 
> Установка через оркестратор автоматически настраивает боевой режим без демо-данных.
> Ниже приведены шаги для ручной установки при необходимости.

### Подготовка рабочей директории
```bash
mkdir akvorado && cd akvorado
curl -sL https://github.com/akvorado/akvorado/releases/latest/download/docker-compose-quickstart.tar.gz | tar zxvf -
```

### Конфигурация
Отредактируйте .env файл:
```bash
vim .env
```

Закомментируйте строку с упоминанием docker-compose-demo.yml:
```
# COMPOSE_FILE=${COMPOSE_FILE}:docker/docker-compose-demo.yml
```

Отредактируйте config/akvorado.yaml:
```bash
vim config/akvorado.yaml
```

Закомментируйте последнюю строку файла, чтобы отключить демо-данные:
```yaml
# Закомментируйте следующую строку, чтобы отключить демо-данные
# demo-exporter: !include "demo.yaml"
```

### Исправление конфигурации JMX для Kafka

В файле docker/docker-compose.yml найдите секцию Kafka и исправьте параметр JMX_PORT, чтобы избежать конфликтов портов:

```yaml
kafka:
  extends:
    file: versions.yml
    service: kafka
  environment:
    - KAFKA_ZOOKEEPER_PROTOCOL=PLAINTEXT
    - KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181
    - KAFKA_CFG_DELETE_TOPIC_ENABLE=true
    - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092
    - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT
    - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
    - KAFKA_CFG_INTER_BROKER_LISTENER_NAME=PLAINTEXT
    - JMX_PORT=5556  # Изменить с 5555 на 5556
```

> **Совет**: С помощью оркестратора это изменение выполняется автоматически: `./kentavra/run fix jmx`

### Запуск сервиса
```bash
# Запуск всех сервисов
docker compose up -d --force-recreate --remove-orphans

# Проверка статуса контейнеров
docker ps

# Просмотр логов
docker compose logs -f
```

> **Совет**: Оркестратор запускает сервисы в правильном порядке с необходимыми задержками между ними: `./kentavra/run start`

## Настройка SNMP для мониторинга сетевого оборудования

> **Примечание**: Вы можете настроить SNMP с помощью оркестратора: `./kentavra/run snmp-setup`

Akvorado может использовать SNMP для опроса сетевого оборудования и обогащения данных о потоках.

### 1. Установка и настройка SNMP на локальном хосте

```bash
# Установка SNMP-демона на Ubuntu
apt-get update
apt-get install snmpd snmp

# Настройка SNMP
cp /etc/snmp/snmpd.conf /etc/snmp/snmpd.conf.backup
nano /etc/snmp/snmpd.conf
```

Замените содержимое файла snmpd.conf на:

```bash
# Прослушивание на всех интерфейсах
agentAddress udp:161,udp6:[::1]:161

# Доступ по SNMP v2c
rocommunity public localhost
rocommunity public 172.20.0.0/16

# Доступ по SNMP v3
createUser akvorado SHA myAuthPassword AES myPrivPassword
rouser akvorado authpriv

# Системная информация
sysLocation    Data Center
sysContact     admin@example.com
sysName        localhost

# Включение мониторинга интерфейсов
view systemview included .1.3.6.1.2.1.1
view systemview included .1.3.6.1.2.1.2
view systemview included .1.3.6.1.2.1.25.1.1
```

Перезапустите SNMP-демон:
```bash
systemctl restart snmpd
systemctl status snmpd
```

### 2. Проверка работы SNMP

```bash
# Проверка с помощью SNMPv2c
snmpwalk -v 2c -c public localhost .1.3.6.1.2.1.1.1.0

# Проверка с помощью SNMPv3
snmpwalk -v 3 -u akvorado -l authPriv -a SHA -A myAuthPassword -x AES -X myPrivPassword localhost .1.3.6.1.2.1.1.1.0
```

### 3. Настройка SNMP в Akvorado

Отредактируйте файл config/akvorado.yaml или config/inlet.yaml, добавив или изменив секцию SNMP:

```yaml
inlet:
  snmp:
    cacheduration: 30m0s
    cacherefresh: 1h0m0s
    cachecheckinterval: 2m0s
    cachepersistfile: "/run/akvorado/snmp_cache"
    pollerretries: 1
    pollertimeout: 1s
    pollercoalesce: 10
    workers: 3
    
    # Настройка SNMPv2c
    communities:
      192.168.0.0/16: public
      172.20.0.0/16: public
      127.0.0.1/32: public
      
    # Настройка SNMPv3
    securityparameters:
      # Настройка для конкретного IP
      127.0.0.1:
        user-name: akvorado
        authentication-protocol: SHA
        authentication-passphrase: myAuthPassword
        privacy-protocol: AES
        privacy-passphrase: myPrivPassword
      
      # Настройка по умолчанию
      default:
        user-name: akvorado
        authentication-protocol: SHA
        authentication-passphrase: myAuthPassword
        privacy-protocol: AES
        privacy-passphrase: myPrivPassword
```

### 4. Перезапуск Akvorado с новой конфигурацией

```bash
# Перезапуск всех сервисов
docker compose restart
```

### 5. Проверка работы SNMP в Akvorado

```bash
# Просмотр логов inlet для проверки SNMP
docker compose logs -f akvorado-inlet | grep -i 'snmp'

# Проверка метрик SNMP
curl -s http://localhost:8080/api/v0/inlet/metrics | grep snmp
```

## Диагностика и устранение неполадок

> **Совет**: Для автоматической диагностики используйте скрипт оркестратора: `./kentavra/run debug`
> или скрипт `./kentavra/check` для расширенной диагностики.

### 1. Проверка статуса компонентов

#### Общая проверка сервисов
```bash
# Проверка состояния всех контейнеров
docker compose ps

# Просмотр логов всех сервисов
docker compose logs -f

# Просмотр логов конкретного сервиса
docker compose logs -f akvorado-orchestrator
docker compose logs -f akvorado-console
docker compose logs -f akvorado-inlet
docker compose logs -f kafka
docker compose logs -f clickhouse
docker compose logs -f redis
```

> **Совет с оркестратором**: `./kentavra/run logs [имя_сервиса]`

#### Проверка работы Kafka и Zookeeper
```bash
# Проверка состояния Zookeeper
docker compose logs -f zookeeper | grep -i 'error\|exception'
docker exec -it akvorado-zookeeper zkServer.sh status

# Проверка состояния Kafka
docker compose logs -f kafka | grep -i 'error\|exception'

# Проверка соединения Kafka с Zookeeper
docker exec -it akvorado-kafka nc -zv zookeeper 2181

# Проверка наличия топика flows и данных в нем (без JMX)
docker exec -it akvorado-kafka env -u JMX_PORT kafka-topics.sh --bootstrap-server kafka:9092 --list
docker exec -it akvorado-kafka env -u JMX_PORT kafka-topics.sh --bootstrap-server kafka:9092 --describe --topic flows

# Проверка консьюмеров
docker exec -it akvorado-kafka env -u JMX_PORT kafka-consumer-groups.sh --bootstrap-server kafka:9092 --list

# Проверка наличия сообщений в топике
docker exec -it akvorado-kafka env -u JMX_PORT kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic flows --from-beginning --max-messages 5
```

> **Совет с оркестратором**: `./kentavra/run kafka-topic list` или `./kentavra/run kafka-topic describe flows`

#### Проверка DNS и сетевых соединений
```bash
# Проверка DNS-разрешения внутри контейнеров
docker exec -it akvorado-inlet ping -c 3 zookeeper
docker exec -it akvorado-inlet ping -c 3 kafka
docker exec -it akvorado-inlet ping -c 3 clickhouse
docker exec -it akvorado-inlet ping -c 3 akvorado-orchestrator

# Проверка сетевых соединений
docker network inspect akvorado_default

# Проверка доступности портов
docker exec -it akvorado-inlet nc -zv kafka 9092
docker exec -it akvorado-inlet nc -zv zookeeper 2181
docker exec -it akvorado-inlet nc -zv clickhouse 9000
docker exec -it akvorado-orchestrator nc -zv kafka 9092
```

> **Совет с оркестратором**: При проблемах с DNS используйте `./kentavra/run fix dns`

#### Проверка работы ClickHouse
```bash
# Подключение к CLI ClickHouse
docker exec -it akvorado-clickhouse clickhouse-client

# Просмотр баз данных и таблиц
SHOW DATABASES;
USE akvorado;
SHOW TABLES;

# Проверка наличия данных
SELECT count() FROM flows;
SELECT min(TimeReceived), max(TimeReceived) FROM flows;

# Проверка последних записей
SELECT * FROM flows ORDER BY TimeReceived DESC LIMIT 5;
```

> **Совет с оркестратором**: `./kentavra/run db-query "SELECT count() FROM akvorado.flows"`

#### Проверка работы Redis
```bash
# Подключение к Redis CLI
docker exec -it akvorado-redis redis-cli

# Проверка работоспособности
PING

# Просмотр ключей и статистики
KEYS *
INFO

# Проверка размера кэша
INFO memory
```

### 2. Решение распространенных проблем

> **Примечание**: Большинство распространенных проблем можно исправить с помощью оркестратора, 
> например: `./kentavra/run fix dns`, `./kentavra/run fix kafka` и т.д.

#### 2.1 Проблемы с Zookeeper и Kafka

**Симптомы**: Ошибки "Session timed out", "Unable to reconnect to ZooKeeper", "UnknownHostException"

**Решение**:

1. **Перезапуск служб в правильном порядке**:
   ```bash
   # Остановка всех контейнеров
   docker compose down
   
   # Запуск сначала Zookeeper
   docker compose up -d zookeeper
   sleep 30  # Подождать загрузки Zookeeper
   
   # Запуск Kafka
   docker compose up -d kafka
   sleep 30  # Подождать загрузки Kafka
   
   # Запуск остальных сервисов
   docker compose up -d
   ```

   > **Совет с оркестратором**: `./kentavra/run restart` (автоматически соблюдает правильный порядок)

2. **Проверка настроек DNS в Docker**:
   ```bash
   # Создание пользовательской сети с явными настройками DNS
   docker network create --driver bridge --subnet=172.20.0.0/16 --gateway=172.20.0.1 akvorado_network
   
   # Использование этой сети в docker-compose.yml
   # Добавьте в файл строку:
   # networks:
   #   default:
   #     external:
   #       name: akvorado_network
   ```

   > **Совет с оркестратором**: `./kentavra/run fix dns`

3. **Исправление ошибки JMX-порта**:
   ```bash
   # Изменение JMX_PORT в docker-compose.yml на 5556
   # Или полное отключение JMX при запуске команд
   docker exec -it akvorado-kafka env -u JMX_PORT kafka-topics.sh --bootstrap-server kafka:9092 --list
   ```

   > **Совет с оркестратором**: `./kentavra/run fix jmx`

#### 2.2 Данные не поступают от inlet в Kafka

**Причины и решения:**

1. **Проверка получения данных inlet-сервисом**:
   ```bash
   # Проверка входящего трафика на портах
   tcpdump -i any port 2055 or port 4739 or port 6343 -n -c 10
   
   # Проверка логов inlet
   docker compose logs -f akvorado-inlet | grep -i 'received\|decode'
   ```

2. **Генерация тестового трафика NetFlow/sFlow**:
   ```bash
   # Установка softflowd для тестирования
   apt-get install softflowd
   
   # Настройка softflowd для отправки NetFlow
   softflowd -i eth0 -d -s 2 -t general=60 -t udp=30 -t tcp=30 -n 127.0.0.1:2055
   ```

   > **Совет с оркестратором**: `./kentavra/run test softflowd` (генерирует тестовые данные)

3. **Проверка конфигурации inlet**:
   ```bash
   # Просмотр конфигурации inlet
   docker exec akvorado-inlet akvorado inlet config
   
   # Просмотр статистики inlet
   curl -s http://localhost:8080/api/v0/inlet/metrics | grep flow
   ```

4. **Проверка соединения inlet с Kafka**:
   ```bash
   # Проверка сетевого соединения
   docker exec akvorado-inlet ping -c 3 kafka
   
   # Проверка порта Kafka
   docker exec akvorado-inlet nc -zv kafka 9092
   ```

5. **Решение проблемы с conntrack (частая проблема в Docker)**:
   ```bash
   # Сброс таблицы conntrack для UDP-портов inlet
   conntrack -D -p udp --orig-port-dst 2055
   conntrack -D -p udp --orig-port-dst 4739
   conntrack -D -p udp --orig-port-dst 6343
   ```

   > **Совет с оркестратором**: `./kentavra/run fix conntrack`

#### 2.3 Данные есть в Kafka, но не попадают в ClickHouse

1. **Проверка Orchestrator (отвечает за перенос данных из Kafka в ClickHouse)**:
   ```bash
   # Логи оркестратора
   docker compose logs -f akvorado-orchestrator | grep -i 'error\|exception\|clickhouse'
   
   # Проверка метрик
   curl -s http://localhost:8080/api/v0/orchestrator/metrics | grep clickhouse
   ```

2. **Проверка соединения с ClickHouse**:
   ```bash
   # Проверка доступности ClickHouse из Orchestrator
   docker exec akvorado-orchestrator curl -s clickhouse:8123/ping
   ```

3. **Проверка схемы таблиц ClickHouse**:
   ```bash
   docker exec -it akvorado-clickhouse clickhouse-client --query="SHOW CREATE TABLE akvorado.flows"
   ```

4. **Проверка ошибок в ClickHouse**:
   ```bash
   docker exec -it akvorado-clickhouse clickhouse-client --query="SELECT last_error_time, last_error_message FROM system.errors ORDER BY last_error_time LIMIT 10 FORMAT Vertical"
   ```

   > **Совет с оркестратором**: `./kentavra/run fix clickhouse`

#### 2.4 Данные есть в ClickHouse, но не отображаются в веб-интерфейсе

1. **Проверка сервиса Console**:
   ```bash
   # Логи консоли
   docker compose logs -f akvorado-console | grep -i 'error\|exception'
   
   # Проверка соединения с ClickHouse
   docker exec akvorado-console curl -s clickhouse:8123/ping
   ```

2. **Проверка интеграции с Grafana**:
   ```bash
   # Логи Grafana
   docker compose logs -f grafana
   ```

### 3. Полезные команды для восстановления

```bash
# Полный перезапуск с сохранением данных
docker compose restart

# Перезапуск с очисткой данных (только для тестового окружения)
docker compose down -v && docker compose up -d

# Принудительный перезапуск компонентов в правильном порядке
docker compose stop
docker compose up -d zookeeper
sleep 30
docker compose up -d kafka
sleep 30
docker compose up -d redis clickhouse
sleep 30
docker compose up -d akvorado-orchestrator
sleep 10
docker compose up -d akvorado-inlet akvorado-console

# Сброс кэша и метаданных (при проблемах с metadata)
docker compose down
rm -rf /var/lib/docker/volumes/akvorado_akvorado-run
docker compose up -d
```

> **Совет с оркестратором**: `./kentavra/run restart` или `./kentavra/run clean && ./kentavra/run start`

### 4. Сбор диагностической информации для отчета о проблеме

```bash
# Сохранение конфигурации и логов
mkdir -p ~/akvorado-debug/{logs,config}

# Сохранение логов
docker compose logs > ~/akvorado-debug/logs/all-services.log
for service in akvorado-inlet akvorado-orchestrator akvorado-console kafka clickhouse redis zookeeper; do
  docker compose logs $service > ~/akvorado-debug/logs/$service.log
done

# Сохранение конфигурации
cp akvorado.yaml ~/akvorado-debug/config/
cp .env ~/akvorado-debug/config/
docker compose config > ~/akvorado-debug/config/docker-compose-expanded.yaml

# Версии компонентов
docker exec akvorado-console akvorado version > ~/akvorado-debug/version.txt

# Проверка сетевых настроек
docker network inspect akvorado_default > ~/akvorado-debug/network.txt

# Архивирование (не включает чувствительные данные)
tar -czf akvorado-debug.tar.gz ~/akvorado-debug
```

> **Совет с оркестратором**: `./kentavra/run debug` (автоматически запускает диагностику)

## Тестирование получения и обработки NetFlow данных

### 1. Генерация тестового NetFlow трафика

```bash
# Установка softflowd для генерации тестовых данных
apt-get install softflowd

# Запуск softflowd для генерации и отправки NetFlow данных
softflowd -i eth0 -d -s 2 -t general=60 -t udp=30 -t tcp=30 -n 127.0.0.1:2055
```

> **Совет с оркестратором**: `./kentavra/run test softflowd` (автоматически генерирует тестовые данные)

### 2. Мониторинг NetFlow/sFlow трафика

```bash
# Мониторинг NetFlow/sFlow трафика с помощью tcpdump
tcpdump -i any port 2055 or port 4739 or port 6343 -n
```

> **Совет с оркестратором**: `./kentavra/run test tcpdump` (запускает мониторинг трафика)

### 3. Проверка получения данных Inlet'ом

```bash
# Проверка логов inlet
docker compose logs -f akvorado-inlet | grep -i 'flow\|received'

# Проверка метрик
curl -s http://localhost:8080/api/v0/inlet/metrics | grep flow_packets_received

# Проверка получения потоков (должен вернуть поток)
curl -s http://localhost:8080/api/v0/inlet/flows?limit=1
```

### 4. Проверка записи данных в Kafka

```bash
# Проверка существования топика flows
docker exec -it akvorado-kafka env -u JMX_PORT kafka-topics.sh --bootstrap-server kafka:9092 --list

# Просмотр сообщений в топике
docker exec -it akvorado-kafka env -u JMX_PORT kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic flows --from-beginning --max-messages 5
```
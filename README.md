# TelegramWorker

## Running 

После скачивания репозитория, не забудьте выполнить установку зависимостей:
```shell
pip3 install -r requirements.txt
```

Затем нужно создать файл config.json, следующего содержания:

```json
{
  "telegram_api_id": "api-id",
  "telegram_api_hash": "api-hash",
  "webhook": "webhook-url (смотри ниже)",
  "storage": "channels", 
  "host": "your-host",
  "port": "your-port",
  "max_channels": "max channels"
}
```

Параметр `storage` содержит имя хранилища списка добавленных каналов. Рекомендуется оставить `channels`

Для запуска системы достаточно выполнить команду:
```shell
python main.py
```
При первом запуске необходимо авторизоваться в Telegram, введя телефон и код из сообщения. 

Чтобы получить актуальный список добавленных каналов выполните
```shell
cat your_storage_name
```

## Using

### AddChannelRequest

#### POST <http://$url/add-channel/$channel>

#### Успешно 

```
201 Created 
208 Already Reported
```

#### Ошибка

```
507 Insufficient Storage (Добавленно максимальное количество каналов)
500 Internal Server Error 
```

### DelChannelRequest

#### POST <http://$url/del-channel/$channel>

#### Успешно 

```
205 Reset Content
```

#### Ошибка

```
404 Not Found
500 Internal Server Error 
```

### Webhook

Сервер будет автоматически собирать посты с добавленных телеграм каналов и отправлять их по адресу указанному в config.json webhook POST запросом.

Структура запроса:
```json
{
  "channel": "forbesrussia",
  "text": "post text"
}
```


# TelegramWorker

## Running 

```shell
python main.py
```
При первом запуске необходимо авторизоваться в Telegram, введя телефон и код из сообщения. 

Чтобы получить актуальный список добавленных каналов выполните

```shell
cat channels
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


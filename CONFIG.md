# Организация конфигураций в Python проектах.

При разработке программного обеспечения часто встает вопрос правильной организации конфигурационных данных приложения. 
Правильное структурирование конфигурационных данных - это не только вопрос удобства разработки, но и безопасности тоже. 
Невнимательный разработчик может случайно запушить секретные конфигурационные данные (такие, как секретный ключ, 
данные для подключения к БД и т.п.) в публичный репозиторий на GitHub или BitBucket, что может создать проблемы для всей команды. 
Чтобы избежать таких случаев нужно с умом подходить к вопросу организации и управления конфигурациями приложения. 
В этой статье мы рассмотрим несколько способов организации конфигурационных данных в приложениях на языке программирования Python, 
а именно:

- Структуры данных языка Python.
- Внешиние конфигурационные файлы.
- Переменные окружения.
- Сторонние библиотеки.


### Стуктуры данных языка Python
Самый простой и очевидный способ, который приходит в голову сразу же - это встроенные структуры данных, языка Python. 
Наиболее ценными в этом смысле являются такие структуры данных, как `dict` и `tuple` (в некоторых случаях и `namedtuple`). 
К примеру, давайте представим, что нам нужно сохранить конфигурационные данные приложения, которое подключается к БД и выполняет некоторый запрос.
Структура проекта будет выглядеть просто:
```
.
├── app
│   ├── __init__.py
│   └── main.py
├── config.py
└── README.md
```

Сразу же можно выделить данные, которые нужно вынести в отдельный модуль - это данные для подключения к БД.

```python
# config.py
import os

DATABASE = {
    'DB_USER': os.environ.get('DB_USER'),
    'DB_PASS': os.environ.get('DB_PASSWORD'),
    'DB_NAME': 'test_db',
    'DB_PORT': '',
    'DB_HOST': '127.0.0.1',
}
```

Теперь непосредственно основная логика:

```python
# main.py
import asyncio
import asyncpg

import config


async def run(query: str):
    conn = await asyncpg.connect(
        user=config.DATABASE['DB_USER'],
        password=config.DATABASE['DB_PASS'],
        database=config.DATABASE['DB_NAME'],
        host=config.DATABASE['DB_HOST'],
        port=config.DATABASE['DB_PORT']
    )
    __ = await conn.fetch(query)
    await conn.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run('''SELECT * FROM users'''))
```

Самый главный выигрыш, который мы получаем, когда выносим конфигурационные данные в отдельный модуль - это возможность 
повтороного использования из любой точки приложения. В случае, если вы обновите конфигурационные 
данные, вам не нужно будет бегать по файлу и исправлять все вручную, вместо этого вы лишь поправите несколько строк 
в модуле с конфигурациями.

Что, если конфигурационыне данные отличаются для различных этапов приложения, т.е мы можем 
иметь разные базы для тестирования, разработки, продакшена? В таких случаях правильным решением будет прибегнуть к 
подходу конфигурирования, принятому в Flask, где все необходимые данные хранятся в классах, соответствующих тому или 
иному этапу разработки.

Давайте перепишем наш модуль config.py с использованием классов в качестве структур для хранения данных.

```python
# config.py
import os


class BaseConfig(object):
    DB_USER = os.environ['DB_USER']
    DB_PASS = os.environ['DB_PASS']
    DB_NAME = os.environ['DB_NAME']
    DB_PORT = 5432
    DB_HOST = ''


class DevelopmentConfig(BaseConfig):
    DB_USER = 'some_dev_user'
    DB_PASS = 'some_dev_pass'
    DB_NAME = 'some_db_name'
    DB_HOST = '127.0.0.1'
    DB_PORT = 1486


class TestingConfig(DevelopmentConfig):
    DB_USER = 'some_test_user'
    DB_PASS = 'some_test_pass'
    DB_NAME = 'some_db_name'


class ProductionConfig(BaseConfig):
    DB_PORT = ''
    DB_HOST = ''


config = {
    'default': DevelopmentConfig,
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig
}
```

Плюс такого подхода очевиден. Мы можем наследовать необходимые атрибуты и переопределять те атрибуты класса, 
которые должны иметь разные значения в разных классах.

```python
# main.py
import asyncio
import asyncpg

from config import config


async def run(config_name, query: str):
    
    c = config[config_name]

    conn = await asyncpg.connect(
        user=c.DATABASE['DB_USER'],
        password=c.DATABASE['DB_PASS'],
        database=c.DATABASE['DB_NAME'],
        host=c.DATABASE['DB_HOST'],
        port=c.DATABASE['DB_PORT']
    )
    __ = await conn.fetch(query)
    await conn.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Запрос выполнится для dev версии БД. 
    loop.run_until_complete(run('dev', '''SELECT * FROM users'''))
```

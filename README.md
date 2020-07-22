# CBR Django

Простой REST сервис на Django для отображения курса валют по ЦБРФ

### Установка
```
pip install -r requirements.txt
```

### Миграции
```
python manage.py load_currencies 
# загрузить все курсы валют
python manage.py load_records --days 90 
# загрузить для каждого курса записи за последние 90 дней    
```

### Фильтры

Можно фильтровать по полю date
```angular2
http://localhost:8000/api/currency/?date=2020-01-01
[
    {
        "code": "R01010",
        "num_code": 36,
        "char_code": "AUD",
        "nominal": 1,
        "name": "Австралийский доллар",
        "value": 48.0033,
        "date": "2020-04-22"
    },
...
]
```

### Авторизация

По умолчанию включена. Необходимо создать пользователя для работы
```
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
```

### TODO

1. Можно добавить шедулер и каждый новый день обновлять БД.
2. Включить регистрацию нового пользователя
3. Добавить сигнал если нет записи в БД, сходить на cbr и записать   
   
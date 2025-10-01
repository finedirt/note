## Оглавление
- [Установка и настройка](# 1. Установка и настройка)
- [Базовое приложение](# 2. Базовое приложение)
- [Основные компоненты](# 3. Основные компоненты)
- [Примеры](#примеры)
- [Лицензия](#лицензия)
# Обучение по библиотеке NiceGUI

NiceGUI - это современная библиотека для создания веб-интерфейсов на Python с минимальным кодом. Вот подробное руководство:

## 1. Установка и настройка

```bash
pip install nicegui
```

## 2. Базовое приложение

```python
from nicegui import ui

# Простейшее приложение
ui.label('Привет, NiceGUI!')
ui.button('Нажми меня', on_click=lambda: ui.notify('Кнопка нажата!'))

ui.run()
```

## 3. Основные компоненты

### Кнопки и события
```python
from nicegui import ui

def handle_click():
    ui.notify(f'Счет: {count}')
    count += 1

count = 0

with ui.row():
    ui.button('Увеличить счет', on_click=handle_click)
    ui.button('Сбросить', on_click=lambda: (globals().update(count=0), ui.notify('Счет сброшен')))
    
ui.number('Введите число', value=0, on_change=lambda e: ui.notify(f'Вы ввели: {e.value}'))

ui.run()
```

### Формы и ввод данных
```python
from nicegui import ui

def submit_form():
    ui.notify(f'Данные: {name.value}, {email.value}, Возраст: {age.value}')
    
with ui.card().classes('w-80 p-4 mx-auto'):
    ui.label('Регистрация').classes('text-2xl font-bold')
    
    name = ui.input('Имя', placeholder='Введите ваше имя')
    email = ui.input('Email', placeholder='email@example.com')
    age = ui.slider(min=0, max=100, value=25)
    ui.label().bind_text_from(age, 'value', lambda value: f'Возраст: {value}')
    
    ui.checkbox('Согласен с условиями')
    
    with ui.row():
        ui.button('Отправить', on_click=submit_form, color='primary')
        ui.button('Очистить', color='secondary')

ui.run()
```

### Работа с данными
```python
from nicegui import ui
from datetime import datetime

# Реактивные переменные
messages = []

def send_message():
    if message_input.value:
        messages.append({
            'text': message_input.value,
            'time': datetime.now().strftime('%H:%M'),
            'user': 'Вы'
        })
        message_input.set_value('')
        update_chat()

def update_chat():
    chat_container.clear()
    with chat_container:
        for msg in messages[-10:]:  # Последние 10 сообщений
            with ui.card().classes('w-full p-2 mb-2'):
                with ui.row().classes('items-center justify-between'):
                    ui.label(msg['user']).classes('font-bold')
                    ui.label(msg['time']).classes('text-xs text-gray-500')
                ui.label(msg['text'])

# Интерфейс чата
with ui.column().classes('w-full max-w-md mx-auto my-4'):
    ui.label('Чат').classes('text-2xl font-bold')
    
    chat_container = ui.column().classes('w-full h-96 border rounded-lg p-4 overflow-y-auto')
    
    with ui.row().classes('w-full'):
        message_input = ui.input(placeholder='Введите сообщение...').classes('flex-grow')
        ui.button('Отправить', on_click=send_message)

ui.run()
```

## 4. Компоновка и стили

```python
from nicegui import ui

with ui.header().classes('bg-blue-500 text-white p-4'):
    ui.label('Мое приложение').classes('text-2xl font-bold')

with ui.left_drawer().classes('bg-gray-100'):
    ui.label('Меню')
    ui.separator()
    ui.button('Главная', icon='home')
    ui.button('Настройки', icon='settings')
    ui.button('Помощь', icon='help')

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(icon='chat', color='primary').classes('w-16 h-16')

with ui.tabs().classes('w-full') as tabs:
    tab1 = ui.tab('Профиль')
    tab2 = ui.tab('Настройки')
    tab3 = ui.tab('Статистика')

with ui.tab_panels(tabs, value=tab1).classes('w-full'):
    with ui.tab_panel(tab1):
        with ui.grid(columns=2).classes('w-full gap-4'):
            with ui.card():
                ui.label('Информация о пользователе').classes('text-xl font-bold')
                ui.input('Имя', value='Иван Иванов')
                ui.input('Email', value='ivan@example.com')
                
            with ui.card():
                ui.label('Статистика').classes('text-xl font-bold')
                ui.linear_progress(value=0.7).classes('w-full')
                ui.label('70% заполнено')
                
    with ui.tab_panel(tab2):
        ui.label('Настройки приложения').classes('text-xl font-bold')
        ui.toggle(['Темная тема', 'Светлая тема'])
        ui.slider(min=0, max=100, value=50).classes('w-full')
        
    with ui.tab_panel(tab3):
        ui.label('Графики и статистика').classes('text-xl font-bold')
        # Здесь можно добавить графики

ui.run()
```

## 5. Графики и визуализация

```python
from nicegui import ui
import random
from datetime import datetime, timedelta

# Генерация случайных данных
dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)]
values = [random.randint(10, 100) for _ in range(30)]

with ui.column().classes('w-full max-w-4xl mx-auto my-4'):
    ui.label('Дашборд с графиками').classes('text-2xl font-bold')
    
    with ui.grid(columns=3).classes('w-full gap-4'):
        with ui.card().classes('p-4'):
            ui.label('Продажи').classes('text-lg font-semibold')
            ui.line_chart(
                {'Продажи': values},
                x=dates
            ).classes('w-full h-48')
            
        with ui.card().classes('p-4'):
            ui.label('Трафик').classes('text-lg font-semibold')
            ui.bar_chart(
                {'Трафик': [random.randint(50, 200) for _ in range(7)]},
                x=['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
            ).classes('w-full h-48')
            
        with ui.card().classes('p-4'):
            ui.label('Производительность').classes('text-lg font-semibold')
            ui.gauge(
                value=75,
                show_value=True
            ).classes('w-full h-48')

ui.run()
```

## 6. Работа с базами данных

```python
from nicegui import ui
import sqlite3
from contextlib import contextmanager

# Утилиты для работы с БД
@contextmanager
def get_db():
    conn = sqlite3.connect('example.db')
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_db()

def load_tasks():
    with get_db() as conn:
        return conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()

def add_task(title, description):
    with get_db() as conn:
        conn.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', (title, description))
        conn.commit()

def delete_task(task_id):
    with get_db() as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()

# Интерфейс менеджера задач
def create_task_manager():
    def refresh_tasks():
        task_list.clear()
        tasks = load_tasks()
        with task_list:
            for task in tasks:
                with ui.card().classes('w-full p-3 mb-2'):
                    with ui.row().classes('items-center justify-between w-full'):
                        with ui.column():
                            ui.label(task[1]).classes('font-bold' + (' line-through' if task[3] else ''))
                            if task[2]:
                                ui.label(task[2]).classes('text-sm text-gray-600')
                        ui.button(icon='delete', color='red').on_click(
                            lambda e, task_id=task[0]: (delete_task(task_id), refresh_tasks())
                        )

    def handle_add_task():
        if title_input.value:
            add_task(title_input.value, desc_input.value)
            title_input.set_value('')
            desc_input.set_value('')
            refresh_tasks()

    with ui.column().classes('w-full max-w-2xl mx-auto my-4'):
        ui.label('Менеджер задач').classes('text-2xl font-bold')
        
        with ui.card().classes('w-full p-4'):
            title_input = ui.input('Название задачи').classes('w-full')
            desc_input = ui.input('Описание').classes('w-full')
            ui.button('Добавить задачу', on_click=handle_add_task, color='primary')
        
        task_list = ui.column().classes('w-full mt-4')
        refresh_tasks()

create_task_manager()
ui.run()
```

## 7. Продвинутые возможности

### WebSocket и реальное время
```python
from nicegui import ui
import asyncio

class RealTimeApp:
    def __init__(self):
        self.clients = set()
        self.messages = []
        
    async def connect(self, client):
        self.clients.add(client)
        await self.update_clients()
        
    async def disconnect(self, client):
        self.clients.discard(client)
        await self.update_clients()
        
    async def send_message(self, message):
        self.messages.append(message)
        for client in self.clients:
            await client.send_json({'type': 'message', 'data': message})
            
    async def update_clients(self):
        for client in self.clients:
            await client.send_json({'type': 'clients_count', 'data': len(self.clients)})

rt_app = RealTimeApp()

@ui.page('/chat')
async def chat_page():
    ui.add_head_html('''
        <style>
            .message { padding: 8px; margin: 4px; border-radius: 8px; }
            .user { background: #e3f2fd; align-self: flex-end; }
            .system { background: #f5f5f5; align-self: center; }
        </style>
    ''')
    
    with ui.column().classes('w-full max-w-md mx-auto h-screen p-4'):
        ui.label('Чат в реальном времени').classes('text-2xl font-bold')
        
        message_container = ui.column().classes('flex-grow border rounded-lg p-4 overflow-y-auto')
        
        with ui.row().classes('w-full'):
            message_input = ui.input(placeholder='Введите сообщение...').classes('flex-grow')
            send_btn = ui.button('Отправить')
            
        # WebSocket соединение
        from nicegui import app
        
        @app.websocket('/ws')
        async def websocket_endpoint(websocket):
            await rt_app.connect(websocket)
            try:
                async for message in websocket:
                    data = await websocket.receive_json()
                    if data['type'] == 'message':
                        await rt_app.send_message(data['data'])
            finally:
                await rt_app.disconnect(websocket)
        
        async def send_message():
            if message_input.value:
                await rt_app.send_message(message_input.value)
                message_input.set_value('')
                
        send_btn.on_click(send_message)

ui.run()
```

### Кастомные компоненты
```python
from nicegui import ui

class CustomCard(ui.card):
    def __init__(self, title: str, content: str, **kwargs):
        super().__init__(**kwargs)
        with self:
            with ui.column().classes('w-full'):
                ui.label(title).classes('text-xl font-bold text-blue-600')
                ui.separator()
                ui.label(content).classes('text-gray-700')
                with ui.row().classes('w-full justify-end'):
                    ui.button('Подробнее', color='primary')
                    ui.button('Закрыть', color='secondary')

# Использование кастомного компонента
with ui.grid(columns=2).classes('w-full max-w-4xl mx-auto gap-4'):
    CustomCard('Заголовок 1', 'Содержание первой карточки с полезной информацией')
    CustomCard('Заголовок 2', 'Содержание второй карточки с дополнительными деталями')
    CustomCard('Заголовок 3', 'Третья карточка с интересным контентом')
    CustomCard('Заголовок 4', 'Четвертая карточка завершает набор')

ui.run()
```

## 8. Деплой приложения

### Локальный запуск
```python
ui.run(
    title='Мое приложение',
    host='0.0.0.0',  # Доступ с других устройств
    port=8080,
    reload=True,  # Автоперезагрузка при изменении кода
    show=True     # Автоматически открыть браузер
)
```

### Конфигурация для продакшена
```python
ui.run(
    title='Production App',
    host='0.0.0.0',
    port=80,
    reload=False,
    show=False,
    uvicorn_logging_level='warning'
)
```

## 9. Советы и лучшие практики

1. **Структура проекта:**
```
my_app/
├── main.py
├── components/
│   ├── __init__.py
│   ├── header.py
│   └── sidebar.py
├── pages/
│   ├── __init__.py
│   ├── dashboard.py
│   └── settings.py
└── utils/
    └── database.py
```

2. **Реактивность:**
```python
# Хорошо - реактивные переменные
counter = ui.number(value=0)
ui.label().bind_text_from(counter, 'value', lambda val: f'Значение: {val}')

# Плохо - прямое обновление
# ui.label(f'Значение: {some_var}')
```

3. **Производительность:**
```python
# Используйте bindings вместо частых обновлений
value = ui.slider(min=0, max=100)
display = ui.label()
display.bind_text_from(value, 'value')
```

## 10. Полезные ресурсы

- [Официальная документация](https://nicegui.io/)
- [Примеры приложений](https://github.com/zauberzeug/nicegui/tree/main/examples)
- [Компоненты UI](https://nicegui.io/documentation)

Это руководство охватывает основные аспекты работы с NiceGUI. Библиотека продолжает развиваться, поэтому рекомендую следить за обновлениями в официальной документации!

from nicegui import ui
from datetime import datetime
import json
import os

class OrderTracker:
    def __init__(self):
        self.data_file = 'orders_data.json'
        self.orders = []
        self.total_amount = 0
        self.list_name = "Мои заказы"
        self.load_data()
    
    def load_data(self):
        """Загружает данные из файла"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.orders = data.get('orders', [])
                    self.list_name = data.get('list_name', 'Мои заказы')
                    self.update_total()
        except Exception as e:
            ui.notify(f"Ошибка загрузки данных: {e}", color='negative')
    
    def save_data(self):
        """Сохраняет данные в файл"""
        try:
            data = {
                'list_name': self.list_name,
                'orders': self.orders,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            ui.notify(f"Ошибка сохранения: {e}", color='negative')
    
    def add_order(self, order_number, amount):
        """Добавляет заказ в список"""
        try:
            amount_float = float(amount)
            if amount_float <= 0:
                ui.notify("Сумма должна быть положительной", color='negative')
                return
                
            self.orders.append({
                'number': order_number.strip(),
                'amount': amount_float,
                'date': datetime.now().strftime('%d.%m %H:%M')
            })
            self.update_total()
            self.refresh_table()
            self.clear_inputs()
            self.save_data()
            ui.notify(f"Заказ {order_number} добавлен!")
        except ValueError:
            ui.notify("Введите корректную сумму", color='negative')
    
    def update_total(self):
        """Обновляет общую сумму"""
        self.total_amount = sum(order['amount'] for order in self.orders)
    
    def refresh_table(self):
        """Обновляет таблицу с заказами"""
        self.table.clear()
        with self.table:
            for i, order in enumerate(self.orders):
                with ui.row().classes('w-full justify-between items-center py-3 px-4 border-b hover:bg-gray-50 transition-colors'):
                    ui.label(f"№{order['number']}").classes('text-lg font-medium w-1/4')
                    ui.label(f"{order['amount']:,.0f} ₽").classes('text-lg font-semibold text-green-600 w-1/4 text-center')
                    ui.label(order['date']).classes('text-sm text-gray-500 w-1/4 text-center')
                    ui.button(icon='delete', color='red', size='sm').on_click(
                        lambda e, index=i: self.delete_order(index)
                    ).classes('w-1/4 justify-center')
    
    def delete_order(self, index):
        """Удаляет конкретный заказ"""
        if 0 <= index < len(self.orders):
            deleted_order = self.orders.pop(index)
            self.update_total()
            self.refresh_table()
            self.save_data()
            ui.notify(f"Заказ №{deleted_order['number']} удален", color='warning')
    
    def clear_inputs(self):
        """Очищает поля ввода"""
        self.order_input.set_value('')
        self.amount_input.set_value('')
    
    def delete_all_orders(self):
        """Удаляет все заказы"""
        if self.orders:
            self.orders.clear()
            self.update_total()
            self.refresh_table()
            self.save_data()
            ui.notify("Все заказы удалены", color='warning')
    
    def export_to_txt(self):
        """Экспортирует данные в TXT файл"""
        try:
            filename = f"{self.list_name.replace(' ', '_')}_заказы.txt"
            content = f"{self.list_name}\n"
            content += "=" * 50 + "\n\n"
            
            for order in self.orders:
                content += f"№{order['number']} - {order['amount']:,.0f} ₽ ({order['date']})\n"
            
            content += f"\n{'=' * 50}\n"
            content += f"ОБЩАЯ СУММА: {self.total_amount:,.0f} ₽\n"
            content += f"Всего заказов: {len(self.orders)}\n"
            content += f"Экспорт: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            
            # Создаем файл для скачивания
            ui.download(content.encode('utf-8'), filename=filename, media_type='text/plain')
            ui.notify(f"Файл {filename} готов к скачиванию!")
            
        except Exception as e:
            ui.notify(f"Ошибка экспорта: {e}", color='negative')
    
    def update_list_name(self):
        """Обновляет название списка"""
        new_name = self.name_input.value.strip()
        if new_name:
            self.list_name = new_name
            self.save_data()
            ui.notify(f"Название списка изменено на: {self.list_name}")
    
    def create_ui(self):
        """Создает пользовательский интерфейс"""
        # Заголовок
        with ui.header().classes('bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'):
            with ui.row().classes('w-full justify-between items-center'):
                with ui.column().classes('gap-1'):
                    ui.label('💰 Трекер заказов').classes('text-2xl font-bold')
                    ui.label().bind_text_from(self, 'list_name').classes('text-sm opacity-90')
                
                with ui.column().classes('items-end gap-1'):
                    ui.label().bind_text_from(self, 'total_amount', 
                                            lambda val: f'Итого: {val:,.0f} ₽').classes('text-xl font-bold bg-white/20 px-4 py-2 rounded-full')
                    ui.label().bind_text_from(self, 'orders', 
                                            lambda orders: f'Заказов: {len(orders)}').classes('text-sm opacity-90')
        
        # Основной контент
        with ui.column().classes('w-full max-w-4xl mx-auto p-6 space-y-6'):
            # Панель управления
            with ui.card().classes('w-full p-4 shadow-lg border-0 bg-gradient-to-br from-gray-50 to-white'):
                with ui.grid(columns=3).classes('w-full gap-4 items-end'):
                    # Название списка
                    with ui.column():
                        ui.label('Название списка').classes('text-sm font-medium text-gray-700')
                        with ui.row().classes('w-full items-center gap-2'):
                            self.name_input = ui.input(value=self.list_name).classes('flex-grow')
                            ui.button(icon='edit', on_click=self.update_list_name, color='blue').classes('px-3')
                    
                    # Экспорт
                    with ui.column():
                        ui.button('📥 Экспорт в TXT', on_click=self.export_to_txt, color='green').classes('w-full bg-gradient-to-r from-green-500 to-emerald-600')
                    
                    # Очистка
                    with ui.column():
                        ui.button('🗑️ Очистить все', on_click=self.delete_all_orders, color='red').classes('w-full')
            
            # Форма добавления заказа
            with ui.card().classes('w-full p-6 shadow-lg border-0 bg-gradient-to-br from-blue-50 to-white'):
                ui.label('Добавить заказ').classes('text-xl font-semibold mb-4 text-gray-800')
                
                with ui.grid(columns=2).classes('w-full gap-4'):
                    self.order_input = ui.input(
                        label='Номер заказа',
                        placeholder='Введите номер заказа...',
                        validation={'Поле обязательно': lambda value: bool(value.strip())}
                    ).classes('w-full')
                    
                    self.amount_input = ui.input(
                        label='Сумма (руб)',
                        placeholder='0',
                        validation={'Введите число': lambda value: value.replace('.', '').replace(',', '').isdigit()}
                    ).classes('w-full')
                
                with ui.row().classes('w-full justify-end gap-2 pt-2'):
                    ui.button('Очистить', on_click=self.clear_inputs, color='gray').classes('px-6')
                    ui.button('Добавить заказ', on_click=lambda: self.add_order(
                        self.order_input.value, 
                        self.amount_input.value
                    ), color='primary').classes('px-6 bg-gradient-to-r from-blue-500 to-purple-600')
            
            # Список заказов
            with ui.card().classes('w-full shadow-lg border-0 overflow-hidden'):
                with ui.column().classes('w-full'):
                    # Заголовок таблицы
                    with ui.row().classes('w-full justify-between items-center py-4 px-4 bg-gray-50 border-b'):
                        ui.label('Заказ').classes('text-sm font-semibold text-gray-600 w-1/4')
                        ui.label('Сумма').classes('text-sm font-semibold text-gray-600 w-1/4 text-center')
                        ui.label('Дата').classes('text-sm font-semibold text-gray-600 w-1/4 text-center')
                        ui.label('Действия').classes('text-sm font-semibold text-gray-600 w-1/4 text-center')
                    
                    # Таблица заказов
                    self.table = ui.column().classes('w-full divide-y')
                    
                    # Сообщение если нет заказов
                    self.empty_state = ui.column().classes('w-full text-center py-16')
                    with self.empty_state:
                        ui.icon('receipt_long', size='xl', color='gray-300').classes('mb-4')
                        ui.label('Нет добавленных заказов').classes('text-gray-400 text-lg mb-2')
                        ui.label('Добавьте первый заказ с помощью формы выше').classes('text-gray-400')
                    
                    # Привязка видимости пустого состояния
                    self.empty_state.bind_visibility_from(self, 'orders', lambda orders: not orders)
        
        # Инициализация таблицы
        self.refresh_table()
        
        # Стили для всего приложения
        ui.add_head_html('''
            <style>
                body {
                    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    margin: 0;
                }
                .nicegui-content {
                    padding: 0 !important;
                    margin: 0 !important;
                }
                .scrollable-table {
                    max-height: 400px;
                    overflow-y: auto;
                }
            </style>
        ''')
    
    def run(self):
        """Запускает приложение"""
        self.create_ui()
        ui.run(
            title='Трекер заказов',
            reload=False,
            port=8080,
            favicon='💰'
        )

# Создаем и запускаем приложение
if __name__ == "__main__":
    app = OrderTracker()
    app.run()

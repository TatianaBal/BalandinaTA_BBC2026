import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QRadioButton, QLineEdit, QPushButton,
                             QCheckBox, QGroupBox, QLabel, QMessageBox,
                             QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt


class TaskManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Менеджер задач")
        self.resize(400, 500)

        # 1. Подключаем БД и создаем таблицу (как на лекции: connect -> cursor -> execute)
        self.init_db()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.label = QLabel("Название задачи:")
        main_layout.addWidget(self.label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите задачу...")
        main_layout.addWidget(self.input_field)

        self.priority_group = QGroupBox("Выбор приоритета")
        priority_layout = QVBoxLayout()
        self.radio_high = QRadioButton("Высокий")
        self.radio_medium = QRadioButton("Средний")
        self.radio_low = QRadioButton("Низкий")
        self.radio_high.setChecked(True)

        priority_layout.addWidget(self.radio_high)
        priority_layout.addWidget(self.radio_medium)
        priority_layout.addWidget(self.radio_low)
        self.priority_group.setLayout(priority_layout)
        main_layout.addWidget(self.priority_group)

        button_layout = QHBoxLayout()
        self.btn_add = QPushButton("Добавить")
        self.btn_clear_done = QPushButton("Удалить выполненные")
        self.btn_clear = QPushButton("Очистить все")
        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_clear_done)
        button_layout.addWidget(self.btn_clear)
        main_layout.addLayout(button_layout)

        self.label_result = QLabel("Список задач:")
        main_layout.addWidget(self.label_result)

        self.task_list = QListWidget()
        main_layout.addWidget(self.task_list)

        self.btn_add.clicked.connect(self.add_task)
        self.btn_clear_done.clicked.connect(self.clear_done_tasks)
        self.btn_clear.clicked.connect(self.clear_tasks)

        # 2. Загружаем старые задачи из базы при запуске
        self.load_tasks()

    def init_db(self):
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT NOT NULL,
                is_done INTEGER DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()

    def load_tasks(self):
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, priority, is_done FROM tasks")
        rows = cursor.fetchall()
        conn.close()

        for task_id, title, priority, is_done in rows:
            self.create_task_widget(task_id, title, priority, bool(is_done))

    def create_task_widget(self, task_id, title, priority, is_done=False):
        task_text = f"[{priority}] {title}"
        item = QListWidgetItem()
        checkbox = QCheckBox(task_text)
        checkbox.setChecked(is_done)
        self.mark_as_done(checkbox, is_done, task_id, save_to_db=False)

        self.task_list.addItem(item)
        self.task_list.setItemWidget(item, checkbox)
        item.setSizeHint(checkbox.sizeHint())

        checkbox.toggled.connect(
            lambda checked, ch=checkbox, tid=task_id: self.mark_as_done(ch, checked, tid, save_to_db=True)
        )

    def add_task(self):
        text = self.input_field.text().strip()
        if not text:
            QMessageBox.warning(self, "Ошибка", "Поле ввода не может быть пустым!")
            return

        if self.radio_high.isChecked():
            priority = "высокий"
        elif self.radio_medium.isChecked():
            priority = "средний"
        else:
            priority = "низкий"

        # Сохраняем новую задачу в БД и получаем её id
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, priority, is_done) VALUES (?, ?, 0)",
            (text, priority)
        )
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()

        self.create_task_widget(task_id, text, priority, is_done=False)
        self.input_field.clear()

    def mark_as_done(self, checkbox, is_checked, task_id, save_to_db=True):
        font = checkbox.font()
        font.setStrikeOut(is_checked)
        checkbox.setFont(font)

        if save_to_db:
            conn = sqlite3.connect("tasks.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET is_done = ? WHERE id = ?",
                (1 if is_checked else 0, task_id)
            )
            conn.commit()
            conn.close()

    def clear_tasks(self):
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks")
        conn.commit()
        conn.close()

        self.task_list.clear()

    def clear_done_tasks(self):
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE is_done = 1")
        conn.commit()
        conn.close()

        self.task_list.clear()
        self.load_tasks()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManagerWindow()
    window.show()
    sys.exit(app.exec())

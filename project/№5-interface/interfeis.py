import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout,QRadioButton, QLineEdit, QPushButton,
                            QCheckBox, QGroupBox,QLabel, QMessageBox,
                            QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt

class TaskManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Менеджер задач")
        self.resize(400,500)
        
        central_widget=QWidget()
        self.setCentralWidget(central_widget)
        main_layout=QVBoxLayout(central_widget)

        self.label=QLabel("Название задачи:")
        main_layout.addWidget(self.label)

        self.input_field=QLineEdit()
        self.input_field.setPlaceholderText("Введите задачу...")
        main_layout.addWidget(self.input_field)

        self.priority_group=QGroupBox("Выбор приоритета")
        priority_layout=QVBoxLayout()
        self.radio_high=QRadioButton("Высокий")
        self.radio_medium=QRadioButton("Средний")
        self.radio_low=QRadioButton("Низкий")
        self.radio_high.setChecked(True)
        priority_layout.addWidget(self.radio_high)
        priority_layout.addWidget(self.radio_medium)
        priority_layout.addWidget(self.radio_low)
        self.priority_group.setLayout(priority_layout)
        main_layout.addWidget(self.priority_group)

        button_layout=QHBoxLayout()
        self.btn_add=QPushButton("Добавить")
        self.btn_clear=QPushButton("Очистить всё")
        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_clear)
        main_layout.addLayout(button_layout)

        self.label_result=QLabel("Список задач:")
        main_layout.addWidget(self.label_result)

        self.task_list = QListWidget()
        main_layout.addWidget(self.task_list)


        self.btn_add.clicked.connect(self.add_task)
        self.btn_clear.clicked.connect(self.clear_tasks)

    def add_task(self):
        text=self.input_field.text().strip()

        if not text:
            QMessageBox.warning(self, "Ошибка", "Поле ввода не может быть пустым!")
            return
        
        if self.radio_high.isChecked():
            priority = "высокий"
        elif self.radio_medium.isChecked():
            priority = "средний"
        else:
            priority = "низкий"

        
        task_text=f"[{priority}]{text}"

        item=QListWidgetItem()
        checkbox=QCheckBox(task_text)
        self.task_list.addItem(item)
        self.task_list.setItemWidget(item,checkbox)
        item.setSizeHint(checkbox.sizeHint())
        checkbox.toggled.connect(lambda checked, cb=checkbox:self.mark_as_done(cb,checked))
        self.input_field.clear()

    def mark_as_done(self,checkbox,is_checked):
        font=checkbox.font()
        font.setStrikeOut(is_checked)
        checkbox.setFont(font)

    def clear_tasks(self):
        self.task_list.clear()

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=TaskManagerWindow()
    window.show()
    sys.exit(app.exec())
        
        
        

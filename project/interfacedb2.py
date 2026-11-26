import tkinter as tk
from tkinter import messagebox
import sqlite3


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер задач (Tkinter + SQLite)")
        self.root.geometry("450x500")

        self.task_ids = []

        # Подключаем БД и создаем таблицу
        self.init_db()

        # Поле ввода
        self.input_field = tk.Entry(root, width=45)
        self.input_field.pack(pady=10)

        # Подсказка внутри поля ввода
        self.input_field.insert(0, "Введите задачу...")
        self.input_field.bind("<FocusIn>", self.clear_placeholder)
        self.input_field.bind("<FocusOut>", self.add_placeholder)

        # Выбор приоритета
        priority_frame = tk.LabelFrame(root, text="Выбор приоритета", padx=10, pady=10)
        priority_frame.pack(pady=5, fill="x", padx=10)

        self.priority_var = tk.StringVar(value="Низкий")
        tk.Radiobutton(priority_frame, text="Высокий", variable=self.priority_var, value="Высокий").pack(side="left", padx=5)
        tk.Radiobutton(priority_frame, text="Средний", variable=self.priority_var, value="Средний").pack(side="left", padx=5)
        tk.Radiobutton(priority_frame, text="Низкий", variable=self.priority_var, value="Низкий").pack(side="left", padx=5)

        # Кнопки управления
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.btn_add = tk.Button(btn_frame, text="Добавить", command=self.add_task, bg="#4CAF50", fg="white")
        self.btn_add.pack(side="left", padx=4)

        self.btn_clear_done = tk.Button(btn_frame, text="Удалить выполненные", command=self.clear_done_tasks, bg="#FF9800", fg="white")
        self.btn_clear_done.pack(side="left", padx=4)

        self.btn_clear = tk.Button(btn_frame, text="Очистить всё", command=self.clear_tasks, bg="#f44336", fg="white")
        self.btn_clear.pack(side="left", padx=4)

        # Список задач
        tk.Label(root, text="Список задач (двойной клик — отметить выполненной):").pack(anchor="w", padx=10)

        self.task_list = tk.Listbox(root, height=15, width=55, selectmode=tk.SINGLE)
        self.task_list.pack(pady=5, padx=10, fill="both", expand=True)

        # Двойной клик для отметки "выполнено"
        self.task_list.bind("<Double-Button-1>", self.mark_as_done)

        # Загружаем сохраненные задачи из базы при запуске
        self.load_tasks()

    def init_db(self):
        conn = sqlite3.connect("tasks_tk.db")
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
        self.task_list.delete(0, tk.END)
        self.task_ids.clear()

        conn = sqlite3.connect("tasks_tk.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, priority, is_done FROM tasks")
        rows = cursor.fetchall()
        conn.close()

        for task_id, title, priority, is_done in rows:
            self.task_ids.append(task_id)
            if is_done:
                self.task_list.insert(tk.END, f"✔ [{priority}] {title}")
                self.task_list.itemconfig(tk.END, fg="gray")
            else:
                self.task_list.insert(tk.END, f"[{priority}] {title}")
                self.task_list.itemconfig(tk.END, fg="black")

    def clear_placeholder(self, event):
        if self.input_field.get() == "Введите задачу...":
            self.input_field.delete(0, tk.END)

    def add_placeholder(self, event):
        if not self.input_field.get():
            self.input_field.insert(0, "Введите задачу...")

    def add_task(self):
        text = self.input_field.get().strip()
        if not text or text == "Введите задачу...":
            messagebox.showwarning("Ошибка", "Поле ввода не может быть пустым!")
            return

        priority = self.priority_var.get()

        conn = sqlite3.connect("tasks_tk.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, priority, is_done) VALUES (?, ?, 0)",
            (text, priority)
        )
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()

        self.task_ids.append(task_id)
        self.task_list.insert(tk.END, f"[{priority}] {text}")
        self.input_field.delete(0, tk.END)

    def mark_as_done(self, event):
        selection = self.task_list.curselection()
        if selection:
            index = selection[0]
            task_id = self.task_ids[index]
            task_text = self.task_list.get(index)

            if task_text.startswith("✔ "):
                new_text = task_text.replace("✔ ", "", 1)
                new_status = 0
                color = "black"
            else:
                new_text = f"✔ {task_text}"
                new_status = 1
                color = "gray"

            # Обновляем статус в БД
            conn = sqlite3.connect("tasks_tk.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET is_done = ? WHERE id = ?", (new_status, task_id))
            conn.commit()
            conn.close()

            # Обновляем строку на экране
            self.task_list.delete(index)
            self.task_list.insert(index, new_text)
            self.task_list.itemconfig(index, fg=color)
            self.task_list.selection_set(index)

    def clear_done_tasks(self):
        conn = sqlite3.connect("tasks_tk.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE is_done = 1")
        conn.commit()
        conn.close()

        self.load_tasks()

    def clear_tasks(self):
        conn = sqlite3.connect("tasks_tk.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks")
        conn.commit()
        conn.close()

        self.task_list.delete(0, tk.END)
        self.task_ids.clear()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

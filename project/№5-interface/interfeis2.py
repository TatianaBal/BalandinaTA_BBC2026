import tkinter as tk
from tkinter import messagebox, font

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер задач")
        self.root.geometry("400x500")

        # Поле ввода и кнопка добавления
        self.input_field = tk.Entry(root, width=40)
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
        
        self.btn_add = tk.Button(btn_frame, text="Добавить задачу", command=self.add_task, bg="#4CAF50", fg="white")
        self.btn_add.pack(side="left", padx=5)
        
        self.btn_clear = tk.Button(btn_frame, text="Очистить всё", command=self.clear_tasks, bg="#f44336", fg="white")
        self.btn_clear.pack(side="left", padx=5)

        # Список задач
        tk.Label(root, text="Список задач:").pack(anchor="w", padx=10)
        
        # Создаем Listbox для отображения задач
        self.task_list = tk.Listbox(root, height=15, width=50, selectmode=tk.SINGLE)
        self.task_list.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Привязываем двойной клик по задаче для отметки "выполнено"
        self.task_list.bind("<Double-Button-1>", self.mark_as_done)

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
        task_text = f"[{priority}] {text}"
        
        self.task_list.insert(tk.END, task_text)
        self.input_field.delete(0, tk.END)

    def mark_as_done(self, event):
        selection = self.task_list.curselection()
        if selection:
            index = selection[0]
            task_text = self.task_list.get(index)
            
            # Если задача уже зачеркнута, убираем зачеркивание
            if task_text.startswith("✔ "):
                new_text = task_text.replace("✔ ", "", 1)
                self.task_list.delete(index)
                self.task_list.insert(index, new_text)
                self.task_list.itemconfig(index, fg="black")
            else:
                # Зачеркиваем задачу
                new_text = f"✔ {task_text}"
                self.task_list.delete(index)
                self.task_list.insert(index, new_text)
                self.task_list.itemconfig(index, fg="gray")
            
            self.task_list.selection_set(index)

    def clear_tasks(self):
        self.task_list.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()







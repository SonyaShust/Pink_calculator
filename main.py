import tkinter as tk
from tkinter import messagebox
import math

BG_COLOR = "#fadcff"        # окнo
DISPLAY_BG = "#fdf5ff"      # для поля ввода
BTN_BG = "#c899cd"          # для кнопок
BTN_FG = "#5f2565"          # текст
BTN_ACTIVE_BG = "#ace3dd"   # при нажатии
FONT_MAIN = ("bookman old style", 14)
FONT_DISPLAY = ("bookman old style", 20)


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("350x450")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # Переменная для хранения текста в поле ввода
        self.input_text = tk.StringVar()

        # --- Регистрация функции валидации ---
        validate_cmd = self.root.register(self.validate_input)

        # --- Поле ввода (Дисплей) ---
        self.display = tk.Entry(
            root,
            textvariable=self.input_text,
            font=FONT_DISPLAY,
            bg=DISPLAY_BG,
            fg=BTN_FG,
            bd=0,
            justify="right",
            validate="key",
            validatecommand=(validate_cmd, '%d', '%P', '%S')
        )
        self.display.pack(fill="both", padx=15, pady=15, ipady=10)

        # --- Панель с кнопками ---
        buttons_frame = tk.Frame(root, bg=BG_COLOR)
        buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        buttons = [
            ('C', 0, 0, self.clear), ('√', 0, 1, self.square_root), ('/', 0, 2, lambda: self.click('/')), ('*', 0, 3, lambda: self.click('*')),
            ('7', 1, 0, lambda: self.click('7')), ('8', 1, 1, lambda: self.click('8')), ('9', 1, 2, lambda: self.click('9')), ('-', 1, 3, lambda: self.click('-')),
            ('4', 2, 0, lambda: self.click('4')), ('5', 2, 1, lambda: self.click('5')), ('6', 2, 2, lambda: self.click('6')), ('+', 2, 3, lambda: self.click('+')),
            ('1', 3, 0, lambda: self.click('1')), ('2', 3, 1, lambda: self.click('2')), ('3', 3, 2, lambda: self.click('3')), ('=', 3, 3, self.calculate),
            ('0', 4, 0, lambda: self.click('0')), ('.', 4, 1, lambda: self.click('.')),
        ]

        for (text, row, col, command) in buttons:
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=FONT_MAIN,
                bg=BTN_BG,
                fg=BTN_FG,
                activebackground=BTN_ACTIVE_BG,
                activeforeground=BTN_FG,
                bd=0,
                command=command
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
            buttons_frame.grid_rowconfigure(row, weight=1)
            buttons_frame.grid_columnconfigure(col, weight=1)

        # Обработка нажатия Enter для вычисления
        self.root.bind("<Return>", lambda event: self.calculate())

    # --- Валидация ввода ---
    def validate_input(self, action, value_if_allowed, value_if_denied):
        """
        action: '1' — вставка, '0' — удаление
        value_if_allowed: строка, которая получится, если ввод разрешить
        """
        if action == '0':
            return True

        allowed_chars = set("0123456789.+-*/")
        for char in value_if_allowed:
            if char not in allowed_chars:
                return False

        return True

    # --- Функции логики ---
    def click(self, char):
        """Добавляет символ в поле ввода."""
        current = self.input_text.get()
        self.input_text.set(current + str(char))

    def clear(self):
        """Очищает поле ввода."""
        self.input_text.set("")

    def calculate(self):
        """Вычисляет результат выражения."""
        expression = self.input_text.get()
        if not expression:
            return
        try:
            result = str(eval(expression))
            self.input_text.set(result)
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль невозможно!")
            self.input_text.set("")
        except Exception:
            messagebox.showerror("Ошибка", "Некорректное выражение")
            self.input_text.set("")

    def square_root(self):
        """Вычисляет квадратный корень текущего числа."""
        try:
            current_value = float(self.input_text.get())
            if current_value < 0:
                messagebox.showerror("Ошибка", "Нельзя извлечь корень из отрицательного числа!")
                self.input_text.set("")
            else:
                result = math.sqrt(current_value)
                self.input_text.set(str(result))
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число для извлечения корня")
            self.input_text.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
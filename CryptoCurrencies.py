import requests
import json
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk


# Получаем название базовой валюты из словаря и обновляем метку
def update_b_label(event):
    code = b_combobox.get()
    name = cur_b[code]
    b_label.config(text=name)

# Получаем  название целевой валюты из словаря и обновляем метку
def update_t_label(event):
    code = t_combobox.get()
    name = cur_t[code]
    t_label.config(text=name)

# Функция для запроса к сервису API coingecko.com
def exchange():
    t_code = t_combobox.get()
    b_code = b_combobox.get()
   # Приводим переменные к нижнему регистру для отправки запроса API
    t_code2 = t_code.lower()
    b_code2 = b_code.lower()
    if t_code and b_code:
        try:
            result_text = ""
            response_link = f"https://api.coingecko.com/api/v3/simple/price?ids={t_code2}&vs_currencies={b_code2}"
            response = requests.get(response_link)
            response.raise_for_status()
            data = response.json()
            if t_code2 in data:
                exchange_rate = data[t_code2][b_code2]
                t_name = cur_t[t_code]
                b_name = cur_b[b_code]
                result_text += f"Курс: 1 {t_name} = {exchange_rate:.2f} {b_name}\n"
            else:
                mb.showerror("Ошибка!", f"Валюта {t_code} не найдена!")
                return
            mb.showinfo("Курсы обмена", result_text.strip())
        except Exception as e:
            mb.showerror("Ошибка", f"Произошла ошибка: {e}.")
    else:
        mb.showwarning("Внимание!", "Введите коды валют!")

# Словарь кодов базовых валют и их полных названий
cur_b = {
    'RUB': 'Российский рубль (RUB)',
    'USD': 'Американский доллар (USD)',
    'EUR': 'Евро (EUR)',
    'GBP': 'Британский фунт стерлингов (GBP)',
}

#Словарь кодов целевых криптовалют и их полных названий
cur_t = {
    'Bitcoin': 'Bitcoin (BTC)',
    'Ethereum': 'Ethereum (ETH)',
    'Litecoin': 'Litecoin (LTC)',
    'Cardano': 'Cardano (ADA)',
    'Ripple': 'Ripple (XRP)'
}

# Создание графического интерфейса
window = Tk()
window.title("Курсы обмена криптовалют")
window.geometry("350x350")
window.iconbitmap(default="bitcoin.ico") # Добавляем иконку приложения


Label(text="Базовая валюта").pack(padx=10, pady=10)
b_combobox = ttk.Combobox(values=list(cur_b.keys()))
b_combobox.pack(padx=10, pady=10)
b_combobox.bind("<<ComboboxSelected>>", update_b_label)
b_label = ttk.Label()
b_label.pack(padx=10, pady=10)


Label(text="Целевая валюта").pack(padx=20, pady=20)
t_combobox = ttk.Combobox(values=list(cur_t.keys()))
t_combobox.pack(padx=10, pady=10)
t_combobox.bind("<<ComboboxSelected>>", update_t_label)

t_label = ttk.Label()
t_label.pack(padx=10, pady=10)

Button(text="Получить курс обмена", command=exchange).pack(padx=10, pady=10)

window.mainloop()

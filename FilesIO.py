import json
import os
import pyperclip
import tkinter as tk
from tkinter import *
import requests
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk


history_file = "upload_history.json"


def save_history(file_path, download_link):
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            history = json.load(file)

    history.append({"file_path": os.path.basename(file_path), "download_link": download_link})

    with open(history_file, "w") as file:
        json.dump(history, file, indent=4)


def show_history():
    if not os.path.exists(history_file):
        mb.showinfo("История", "История загрузок пуста")
        return

    history_window = Toplevel(app)
    history_window.title("История загрузок")

    files_listbox = Listbox(history_window, width=80, height=20)
    files_listbox.grid(row=0, column=0, padx=(10), pady=10)

    with open(history_file, "r") as file:
        history = json.load(file)
        for item in history:
            files_listbox.insert(END, f"Файл: {item['file_path']},  Ссылка:  {item['download_link']}")


def upload_file():
    try:
        filepath = fd.askopenfilename()
        if filepath:
            with open(filepath, 'rb') as f:
                files = {'file': f}
                response = requests.post('https://file.io', files=files)
                response.raise_for_status()
                download_link = response.json().get('link')
                if download_link:
                    link_entry.delete(0, tk.END)
                    link_entry.insert(0, download_link)
                    pyperclip.copy(download_link)
                    save_history(filepath, download_link)
                    mb.showinfo("Ссылка скопирована", "Ссылка успешно скопирована в буфер обмена")
                else:
                    raise ValueError("Не удалось получить ссылку для скачивания")
    except requests.RequestException as e:
        mb.showerror("Ошибка сети", f"Произошла ошибка сети: {e}")
    except ValueError as ve:
        mb.showerror("Ошибка", str(ve))
    except Exception as ex:
        mb.showerror("Ошибка", f"Произошла неизвестная ошибка: {ex}")

app = tk.Tk()
app.title("Сохранение файлов в облаке")
app.geometry("360x100")

upload_button = ttk.Button(app, text="Загрузить файл", command=upload_file)
upload_button.pack()

link_entry = ttk.Entry(app)
link_entry.pack()

history_button = ttk.Button(app, text="Посмотреть Историю", command=show_history)
history_button.pack()

app.mainloop()

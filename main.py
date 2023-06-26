import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import psycopg2
import center
from tkinter import filedialog
import requests
import os
from tkinter import ttk
import subprocess

script1_path = os.path.join(os.path.dirname(__file__), "api.py")
script2_path = os.path.join(os.path.dirname(__file__), "web_take_logs.py")

subprocess.Popen(["python", script1_path])
subprocess.Popen(["python", script2_path])

# Данные для POSTGRE SQL
host = '158.160.63.207'
user = 'chapcheliza'
pas = 'admin'
db_name = 'kal'

# Задаем тему
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme('dark-blue')

# Создаем окно емае
root = ctk.CTk()
root.title('Authorization')
root.geometry('600x440')
root.resizable(False, False)

# Функция пост-авторизации
def login_success():
    new_root = ctk.CTk()
    new_root.title("After auth")
    new_root.geometry("400x300")
    new_root.resizable(False, False)

    def choose_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    process_file(file_path)
                messagebox.showinfo('Успех', 'Вы удачно обработали данные!')
            except:
                messagebox.showerror('Ошибка', 'Произошла ошибка, возможно вы выбрали не файл логов')


    def process_file(file_path):
        url = 'http://127.0.0.1:5000/upload_logs'
        file_path = file_path
        with open(file_path, 'rb') as file:
            response = requests.post(url, files={'file': file})


    def static_logs():
        connector = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='pas1',
            database='practice'

        )

        toor = ctk.CTkToplevel()
        toor.geometry('900x900')
        toor.resizable(False, False)

        table = ttk.Treeview(toor)
        table['columns'] = ('column1', 'column2', 'column3', 'column4', 'column5')
        table.heading('column1', text='Id')
        table.heading('column2', text='Timestamp')
        table.heading('column3', text='IP')
        table.heading('column4', text='Method')
        table.heading('column5', text='Status_code')

        table.pack(pady=30)

        with connector.cursor() as cursor:
            cursor.execute('SELECT id, timestamp, ip, method, status_code FROM logs')
            rows = cursor.fetchall()
            for row in rows:
                table.insert('', 'end', values=row)

        def sort_post():
            table.delete(*table.get_children())
            with connector.cursor() as cur:
                cur.execute("SELECT id, timestamp, ip, method, status_code FROM logs where method='POST'")
                rows = cur.fetchall()
                for row in rows:
                    table.insert('', 'end', values=row)
        def sort_get():
            table.delete(*table.get_children())
            with connector.cursor() as cur:
                cur.execute("SELECT id, timestamp, ip, method, status_code FROM logs where method='GET'")
                rows = cur.fetchall()
                for row in rows:
                    table.insert('', 'end', values=row)
        def sort_date():
            table.delete(*table.get_children())
            with connector.cursor() as cur:
                cur.execute("SELECT id, timestamp, ip, method, status_code FROM logs ORDER BY timestamp DESC")
                rows = cur.fetchall()
                for row in rows:
                    table.insert('', 'end', values=row)

        btn_yes = ctk.CTkButton(master=toor, text='Сортировать по Post', command=sort_post)
        btn_yes.pack()
        btn_yes = ctk.CTkButton(master=toor, text='Сортировать по Get', command=sort_get)
        btn_yes.pack()
        btn_yes = ctk.CTkButton(master=toor, text='Сортировать по дате', command=sort_date)
        btn_yes.pack()



    def web_logs():
        connector = psycopg2.connect(
            host=host,
            user=user,
            password=pas,
            database=db_name

        )

        toor = ctk.CTkToplevel()
        toor.geometry('900x900')
        toor.resizable(False, False)

        table = ttk.Treeview(toor)
        table['columns'] = ('column1', 'column2', 'column3', 'column4', 'column5')
        table.heading('column1', text='Id')
        table.heading('column2', text='Timestamp')
        table.heading('column3', text='IP')
        table.heading('column4', text='Method')
        table.heading('column5', text='Status_code')

        table.pack(pady=30)

        with connector.cursor() as cursor:
            cursor.execute('SELECT id, timestamp, ip, method, status_code FROM logs limit 50')
            rows = cursor.fetchall()
            for row in rows:
                table.insert('', 'end', values=row)

        def sort_post():
            table.delete(*table.get_children())
            with connector.cursor() as cur:
                cur.execute("SELECT id, timestamp, ip, method, status_code FROM logs where method='POST'")
                rows = cur.fetchall()
                for row in rows:
                    table.insert('', 'end', values=row)
        def sort_get():
            table.delete(*table.get_children())
            with connector.cursor() as cur:
                cur.execute("SELECT id, timestamp, ip, method, status_code FROM logs where method='GET'")
                rows = cur.fetchall()
                for row in rows:
                    table.insert('', 'end', values=row)
        def sort_date():
            table.delete(*table.get_children())
            with connector.cursor() as cur:
                cur.execute("SELECT id, timestamp, ip, method, status_code FROM logs ORDER BY timestamp DESC")
                rows = cur.fetchall()
                for row in rows:
                    table.insert('', 'end', values=row)

        btn_yes = ctk.CTkButton(master=toor, text='Сортировать по Post', command=sort_post)
        btn_yes.pack()
        btn_yes = ctk.CTkButton(master=toor, text='Сортировать по Get', command=sort_get)
        btn_yes.pack()
        btn_yes = ctk.CTkButton(master=toor, text='Сортировать по дате', command=sort_date)
        btn_yes.pack()



    finall_fr = ctk.CTkFrame(master=new_root, width=300, height=300)
    finall_fr.place(anchor=tk.CENTER, relx=0.5, rely=0.5)

    btn1 = ctk.CTkButton(finall_fr, text="Выбрать файл", command=choose_file)
    btn1.pack(pady=10)

    btn1 = ctk.CTkButton(finall_fr, text="Посмотреть статичные логи", command=static_logs)
    btn1.pack(pady=10)

    btn1 = ctk.CTkButton(finall_fr, text="Посмотреть логи сервера", command=web_logs)
    btn1.pack(pady=10)

    # Центрируем окно
    center.center_window(new_root)
    root.destroy()
    new_root.mainloop()


# Функция логина
def login():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=pas,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute('SELECT login, pass FROM auth')
            rows = cursor.fetchall()

            info = {row[0]: row[1] for row in rows}

            if entry_login.get() == '' or entry_password.get() == '':
                messagebox.showerror('Ошибка', 'Заполните все поля!')
            else:
                login = entry_login.get()
                password = entry_password.get()

                if login in info and password == info[login]:
                    messagebox.showinfo('Успех', 'Успешная авторизация!')
                    login_success()

                else:
                    messagebox.showerror('Ошибка', 'Неверный логин или пароль!')
    except:
        messagebox.showerror('Ошибка', 'Ну тут даже ведьмак не поможет')

# Функция регистрации аккаунта
def registration():
    window = ctk.CTkToplevel(root)
    window.geometry("800x600")
    window.resizable(False, False)

    def reg():
        if entry_password_reg.get() == "" or entry_email_reg.get() == "" or entry_login_reg.get() == "":
            messagebox.showerror("Ошибки", "Вам требуется заполнить все поля")

        else:
            try:
                connect = psycopg2.connect(
                    host=host,
                    user=user,
                    password=pas,
                    database=db_name
                )
                connect.cursor().execute(f"insert into auth(login,pass,email)"
                                         f" values('{entry_login_reg.get()}','{entry_password_reg.get()}','{entry_email_reg.get()}')")
                connect.commit()
                messagebox.showinfo('Успех', 'Аккаунт зарегистрирован')

                window.destroy()
            except:
                messagebox.showerror('Ошибка', 'Возникла непредвиденная ошибка')

    def clear_field():
        for widget in frame.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, 'end')

    reg_title_label = ctk.CTkLabel(master=window, text="Register panel", font=('Century Gothic', 30))
    reg_title_label.pack(pady=10)

    frame = ctk.CTkFrame(master=window, width=600, height=360, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    label_reg = ctk.CTkLabel(master=frame, text="Fill in the fields", font=('Century Gothic', 24))
    label_reg.place(relx=0.36)

    entry_login_reg = ctk.CTkEntry(master=frame, width=220, placeholder_text='Username', font=('Century Gothic', 16))
    entry_login_reg.place(relx=0.1, y=90)

    entry_password_reg = ctk.CTkEntry(master=frame, width=220, placeholder_text='Password', font=('Century Gothic', 16))
    entry_password_reg.place(relx=0.1, y=140)

    entry_email_reg = ctk.CTkEntry(master=frame, width=220, placeholder_text='E-mail', font=('Century Gothic', 16))
    entry_email_reg.place(relx=0.1, y=190)

    button_register = ctk.CTkButton(master=frame, text='Register', width=150, corner_radius=6, command=reg)
    button_register.place(relx=0.70, rely=0.9)
    button_register.configure(fg_color="#262525")

    button_clear = ctk.CTkButton(master=frame, text='Clear fields', width=150, corner_radius=6, command=clear_field)
    button_clear.place(relx=0.05, rely=0.9)
    button_clear.configure(fg_color="#262525")

    # Центрируем окно
    center.center_window(window)
    window.mainloop()

# Просто кнопочки и т.д
frame_log = ctk.CTkFrame(master=root, width=320, height=360, corner_radius=15)
frame_log.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

label_title = ctk.CTkLabel(master=frame_log, text='Authorization', font=('Century Gothic', 20))
label_title.place(x=100, y=45)

entry_login = ctk.CTkEntry(master=frame_log, width=220, placeholder_text='Username', font=('Century Gothic', 16))
entry_login.place(x=50, y=110)

entry_password = ctk.CTkEntry(master=frame_log, width=220, placeholder_text='Password', font=('Century Gothic', 16))
entry_password.place(x=50, y=160)

button_title = ctk.CTkButton(master=frame_log, text='Registration', font=('Century Gothic', 12), command=registration)
button_title.place(x=180, y=190)
button_title.configure(fg_color="#262525")

button_login = ctk.CTkButton(master=frame_log, text='Log in', width=220, corner_radius=6, command=login)
button_login.place(x=50, y=260)
button_login.configure(fg_color="#262525")

# Центрируем окно
center.center_window(root)
root.mainloop()

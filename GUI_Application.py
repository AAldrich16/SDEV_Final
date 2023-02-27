import tkinter as tk
from tkinter import ttk
import subprocess
from ttkthemes import ThemedTk
import sv_ttk
import threading
import json


class App:
    def __init__(self):
        self.root = ThemedTk(theme="dark")
        sv_ttk.set_theme("dark")
        self.root.title("Over Ambitious")

        ## Creating the notebook with two tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        ## Creating the console [Tab 1]
        self.current_tab = tk.Frame(self.notebook)
        self.text_box = tk.Text(self.current_tab)
        self.text_box.pack(fill='both', expand=False)
        self.start_button = ttk.Button(self.current_tab, text="start", command=self.start_script)
        self.start_button.pack(pady=20, padx=20)
        self.stop_button = ttk.Button(self.current_tab, text="stop", command=self.stop_script, state='disable')
        self.stop_button.pack(pady=20, padx=20)
        self.process = None
        self.notebook.add(self.current_tab, text='Bot Console')

        ## Creating the Panel [Tab 2]
        self.form_tab = tk.Frame(self.notebook)
        self.nick_label = ttk.Label(self.form_tab, text="Bot Nick")
        self.nick_label.pack(pady=10)
        self.nick_entry = ttk.Entry(self.form_tab)
        self.nick_entry.pack(pady=5)
        self.avatar_label = ttk.Label(self.form_tab, text="Avatar")
        self.avatar_label.pack(pady=10)
        self.avatar_entry = ttk.Entry(self.form_tab)
        self.avatar_entry.pack(pady=5)
        self.room_label = ttk.Label(self.form_tab, text="Room")
        self.room_label.pack(pady=10)
        self.room_entry = ttk.Entry(self.form_tab)
        self.room_entry.pack(pady=5)
        self.moderation = ttk.Checkbutton(self.form_tab, text='Moderation', onvalue=1, offvalue=0)
        self.moderation.pack()
        self.edit_button = ttk.Button(self.form_tab, text="Edit")
        self.edit_button.pack(pady=20, padx=20)
        self.fill_form()
        self.notebook.add(self.form_tab, text='Bot Panel')

    ## Functions used to Stop, Start and Restart Bot Script
    def start_script(self):
        self.stop_button.config(state='normal')
        self.start_button.config(state='disable')
        self.process = subprocess.Popen(["python", "Bot/bot.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        threading.Thread(target=self.read_output, args=(self.process.stdout,)).start()
        threading.Thread(target=self.read_output, args=(self.process.stderr,)).start()

    def stop_script(self):
        # Killing the script
        self.process.terminate()
        self.text_box.insert('end', "script killed")
        self.stop_button.config(state='disable')
        self.start_button.config(state='normal')

    ## Grabbing and Reading Data from Bot Script
    def read_output(self, output):
        for line in iter(output.readline, b''):
            self.text_box.insert('end', line.decode())
            self.text_box.see('end')

    ## Filling Tab 2 [Panel] with JSON Data
    def fill_form(self):
        with open('data.json') as f:
            data = json.load(f)
            self.nick_entry.insert(0, data['botname'])
            self.avatar_entry.insert(0, data['avatar'])
            self.room_entry.insert(0, data['room'])


app = App()
app.root.mainloop()

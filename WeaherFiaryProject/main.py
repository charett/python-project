Python 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> import tkinter as tk
... from tkinter import messagebox, ttk
... import json
... import os
... from datetime import datetime
... 
... class WeatherDiaryApp:
...     def __init__(self, root):
...         self.root = root
...         self.root.title("Weather Diary")
...         self.root.geometry("700x500")
...         self.file_path = "data.json"
...         self.data = self.load_data()
... 
...         # --- Поля ввода ---
...         frame_input = tk.LabelFrame(root, text="Новая запись")
...         frame_input.pack(fill="x", padx=10, pady=5)
... 
...         tk.Label(frame_input, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
...         self.ent_date = tk.Entry(frame_input)
...         self.ent_date.insert(0, datetime.now().strftime("%d.%m.%Y"))
...         self.ent_date.grid(row=0, column=1, padx=5, pady=5)
... 
...         tk.Label(frame_input, text="Температура (°C):").grid(row=0, column=2)
...         self.ent_temp = tk.Entry(frame_input)
...         self.ent_temp.grid(row=0, column=3, padx=5, pady=5)
... 
...         tk.Label(frame_input, text="Описание:").grid(row=1, column=0)
...         self.ent_desc = tk.Entry(frame_input)
...         self.ent_desc.grid(row=1, column=1, padx=5, pady=5)
... 
...         tk.Label(frame_input, text="Осадки:").grid(row=1, column=2)
...         self.comb_precip = ttk.Combobox(frame_input, values=["Да", "Нет"], state="readonly")
...         self.comb_precip.set("Нет")
...         self.comb_precip.grid(row=1, column=3, padx=5, pady=5)
... 
...         tk.Button(frame_input, text="Добавить запись", command=self.add_record, bg="green", fg="white").grid(row=2, column=0, columnspan=4, sticky="we", padx=5, pady=5)

        # --- Фильтрация ---
        frame_filter = tk.LabelFrame(root, text="Фильтрация")
        frame_filter.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_filter, text="Поиск по дате:").grid(row=0, column=0)
        self.f_date = tk.Entry(frame_filter)
        self.f_date.grid(row=0, column=1, padx=5)

        tk.Label(frame_filter, text="Темп. выше:").grid(row=0, column=2)
        self.f_temp = tk.Entry(frame_filter)
        self.f_temp.grid(row=0, column=3, padx=5)

        tk.Button(frame_filter, text="Применить", command=self.apply_filter).grid(row=0, column=4, padx=5)
        tk.Button(frame_filter, text="Сброс", command=self.update_table).grid(row=0, column=5, padx=5)

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("date", "temp", "desc", "precip"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("desc", text="Описание")
        self.tree.heading("precip", text="Осадки")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_table()

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def add_record(self):
        d, t, ds, p = self.ent_date.get(), self.ent_temp.get(), self.ent_desc.get(), self.comb_precip.get()
        try:
            datetime.strptime(d, "%d.%m.%Y") # Проверка даты
            temp_val = float(t) # Проверка числа
            if not ds: raise ValueError # Проверка описания
            
            self.data.append({"date": d, "temp": temp_val, "desc": ds, "precip": p})
            self.save_data()
            self.update_table()
            self.ent_temp.delete(0, tk.END)
            self.ent_desc.delete(0, tk.END)
        except:
            messagebox.showerror("Ошибка", "Проверьте правильность ввода!")

    def update_table(self, records=None):
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in (records if records is not None else self.data):
            self.tree.insert("", "end", values=(r["date"], r["temp"], r["desc"], r["precip"]))

    def apply_filter(self):
        filtered = self.data
        if self.f_date.get():
            filtered = [r for r in filtered if self.f_date.get() in r["date"]]
        if self.f_temp.get():
            try:
                val = float(self.f_temp.get())
                filtered = [r for r in filtered if r["temp"] > val]
            except: pass
        self.update_table(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()

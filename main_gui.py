# -*- coding: utf-8 -*-
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "books.json"
FONT_NAME = "Tahoma"


class Library:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.books = self._load()

    def _load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def _save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=2)

    def add_book(self, title, author, year):
        self.books.append({"title": title, "author": author, "year": year})
        self._save()

    def remove_book(self, title):
        before = len(self.books)
        self.books = [b for b in self.books if b["title"] != title]
        self._save()
        return len(self.books) < before

    def search_books(self, keyword):
        keyword = keyword.strip().lower()
        return [
            b for b in self.books
            if keyword in b["title"].lower() or keyword in b["author"].lower()
        ]

    def list_books(self):
        return self.books


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.library = Library()

        root.title("سیستم مدیریت کتابخانه")
        root.geometry("640x520")
        root.configure(bg="#f5f5f5")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=(FONT_NAME, 11), padding=6)
        style.configure("Treeview", font=(FONT_NAME, 11), rowheight=28)
        style.configure("Treeview.Heading", font=(FONT_NAME, 11, "bold"))

        self._build_form()
        self._build_buttons()
        self._build_table()
        self._build_search()

        self.refresh_table()

    def _build_form(self):
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(fill="x", padx=15, pady=10)

        tk.Label(frame, text="عنوان:", font=(FONT_NAME, 11), bg="#f5f5f5",
                  anchor="e", justify="right").grid(row=0, column=2, sticky="e", padx=5, pady=4)
        self.title_entry = tk.Entry(frame, font=(FONT_NAME, 11), justify="right")
        self.title_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=4)

        tk.Label(frame, text="نویسنده:", font=(FONT_NAME, 11), bg="#f5f5f5",
                  anchor="e", justify="right").grid(row=1, column=2, sticky="e", padx=5, pady=4)
        self.author_entry = tk.Entry(frame, font=(FONT_NAME, 11), justify="right")
        self.author_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=4)

        tk.Label(frame, text="سال:", font=(FONT_NAME, 11), bg="#f5f5f5",
                  anchor="e", justify="right").grid(row=2, column=2, sticky="e", padx=5, pady=4)
        self.year_entry = tk.Entry(frame, font=(FONT_NAME, 11), justify="right")
        self.year_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=4)

        frame.columnconfigure(1, weight=1)

    def _build_buttons(self):
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(fill="x", padx=15, pady=5)

        ttk.Button(frame, text="افزودن کتاب", command=self.add_book).pack(side="right", padx=4)
        ttk.Button(frame, text="حذف کتاب انتخاب‌شده", command=self.remove_selected).pack(side="right", padx=4)
        ttk.Button(frame, text="پاک کردن فرم", command=self.clear_form).pack(side="right", padx=4)

    def _build_search(self):
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(fill="x", padx=15, pady=5)

        self.search_entry = tk.Entry(frame, font=(FONT_NAME, 11), justify="right")
        self.search_entry.pack(side="right", fill="x", expand=True, padx=5)
        ttk.Button(frame, text="جستجو", command=self.search_books).pack(side="right", padx=4)
        ttk.Button(frame, text="نمایش همه", command=self.refresh_table).pack(side="right", padx=4)
    def _build_table(self):
        columns = ("title", "author", "year")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=12)
        self.tree.heading("title", text="عنوان")
        self.tree.heading("author", text="نویسنده")
        self.tree.heading("year", text="سال")

        self.tree.column("title", anchor="e", width=250)
        self.tree.column("author", anchor="e", width=180)
        self.tree.column("year", anchor="center", width=80)

        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        year = self.year_entry.get().strip()

        if not title or not author or not year:
            messagebox.showwarning("خطا", "لطفاً همه فیلدها را پر کنید.")
            return
        if not year.isdigit():
            messagebox.showwarning("خطا", "سال باید عدد باشد.")
            return

        self.library.add_book(title, author, int(year))
        self.clear_form()
        self.refresh_table()

    def remove_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("توجه", "یک کتاب را از جدول انتخاب کنید.")
            return
        item = self.tree.item(selected[0])
        title = item["values"][0]
        self.library.remove_book(title)
        self.refresh_table()

    def search_books(self):
        keyword = self.search_entry.get().strip()
        results = self.library.search_books(keyword)
        self._fill_table(results)

    def refresh_table(self):
        self._fill_table(self.library.list_books())

    def _fill_table(self, books):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for b in books:
            self.tree.insert("", "end", values=(b["title"], b["author"], b["year"]))

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
  
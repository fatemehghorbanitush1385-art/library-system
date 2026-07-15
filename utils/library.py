# utils/library.py
import json
from pathlib import Path
from utils.book import Book

class Library:
    def __init__(self, filename="books.json"):
        self.filename = filename
        self.books = []
        self.load_books()
    
    def load_books(self):
        """کتاب‌ها رو از JSON بخون"""
        file = Path(self.filename)
        if file.exists():
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = [Book(b["title"], b["author"], b["year"]) for b in data]
    
    def save_books(self):
        """کتاب‌ها رو توی JSON ذخیره کن"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=2)
    
    def add_book(self, title, author, year):
        """کتاب جدید اضافه کن"""
        book = Book(title, author, year)
        self.books.append(book)
        self.save_books()
        print(f"کتاب '{title}' اضافه شد.")
    
    def remove_book(self, title):
        """کتاب رو حذف کن"""
        self.books = [b for b in self.books if b.title != title]
        self.save_books()
        print(f"کتاب '{title}' حذف شد.")
    
    def search_books(self, keyword):
        """کتاب رو جستجو کن"""
        results = [b for b in self.books if keyword.lower() in b.title.lower() or keyword.lower() in b.author.lower()]
        return results
    
    def list_books(self):
        """تمام کتاب‌ها رو نشون بده"""
        if not self.books:
            print("هیچ کتابی وجود ندارد!")
            return
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")
        def search_by_author(self, author):
                                                     """کتاب‌های یک نویسنده رو جستجو کن"""
        results = [b for b in self.books if author.lower() in b.author.lower()]
        if results:
            for book in results:
                print(book)
        else:
            print(f"کتابی از {author} یافت نشد!")
        return results
    def search_by_genre(self, genre):
        """کتاب‌های یک ژانر رو جستجو کن"""
        results = [b for b in self.books if hasattr(b, 'genre') and genre.lower() in b.genre.lower()]
        return results
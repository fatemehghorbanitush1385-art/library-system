# utils/book.py

class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
    
    def __str__(self):
        return f"عنوان: {self.title} | نویسنده: {self.author} | سال: {self.year}"
    
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year
        }
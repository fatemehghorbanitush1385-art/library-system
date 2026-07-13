# -*- coding: utf-8 -*-
from utils.library import Library


def main():
    library = Library()
    
    while True:
        print("\n--- سیستم مدیریت کتابخانه ---")
        print("۱. اضافه کردن کتاب")
        print("۲. حذف کتاب")
        print("۳. جستجو کتاب")
        print("۴. نمایش تمام کتاب‌ها")
        print("۵. خروج")
        
        choice = input("\nانتخاب کنید: ")
        
        if choice == "1":
            title = input("عنوان کتاب: ")
            author = input("نویسنده: ")
            year = int(input("سال: "))
            library.add_book(title, author, year)
        
        elif choice == "2":
            title = input("عنوان کتاب برای حذف: ")
            library.remove_book(title)
        
        elif choice == "3":
            keyword = input("کلمه جستجو: ")
            results = library.search_books(keyword)
            if results:
                for book in results:
                    print(book)
            else:
                print("کتابی یافت نشد!")
        
        elif choice == "4":
            library.list_books()
        
        elif choice == "5":
            print("خروج...")
            break
        
        else:
            print("انتخاب نامعتبر!")

if __name__ == "__main__":
    main()
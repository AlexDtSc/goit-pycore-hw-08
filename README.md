# goit-pycore-hw-08
Homework. Topic 12.  "Тема 12. Management of order of serialization and coping objects". Course "Python programming Foundation and Best practices".


Тема 12. Домашня робота. Серіалізація та копіювання об'єктів в Python



Привіт!

Це фiнальне домашнє завдання, завдяки якому ви навчитеся наступним корисним навичкам:

Серіалізація та десеріалізація даних з використанням pickle
Робота з файлами


Формат здачі:

Розмістіть файли з розв'язанням у репозиторії goit-pycore-hw-08, та прикріпіть лінки до них у відповідь на домашнє завдання.
Прикріпіть файл репозиторію у форматi zip у відповідь на домашнє завдання.
💡 ВАЖЛИВО
Перегляньте Iнструкцію щодо завантаження робочого файлу з репозиторію на Github


Формат оцінювання:

Оцінка від 0 до 100


Поїхали!🚀





Технiчний опис завдання

☝ В цьому домашньому завданні ви повинні додати функціонал збереження адресної книги на диск та відновлення з диска.


Для цього — ви маєте вибрати pickle протокол серіалізації/десеріалізації даних та реалізувати методи, які дозволять зберегти всі дані у файл і завантажити їх із файлу.



Головна мета, щоб застосунок не втрачав дані після виходу із застосунку та при запуску відновлював їх з файлу. Повинна зберігатися адресна книга з якою ми працювали на попередньому сеансі.



Реалізуйте функціонал для збереження стану AddressBook у файл при закритті програми і відновлення стану при її запуску.



Приклади коду, які стануть в нагоді:

Серіалізація з pickle

import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено



Інтеграція збереження та завантаження в основний цикл

def main():
    book = load_data()

    # Основний цикл програми

    save_data(book)  # Викликати перед виходом з програми



Ці приклади допоможуть вам у реалізації домашнього завдання.


Критерії оцінювання:

Реалізовано протокол серіалізації/десеріалізації даних за допомогою pickle
Всі дані повинні зберігатися при виході з програми
При новому сеансі Адресна книга повинна бути у застосунку, яка була при попередньому запуску.

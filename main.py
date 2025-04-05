import pickle
from collections import UserDict
import re                                   # Для валідації номерів телефонів
from datetime import datetime, timedelta

## Базовий клас для всіх полів запису
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

## Клас для зберігання імені контакту (обов'язкове поле)
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")  # Перевірка на порожнє ім'я
        super().__init__(value)

## Клас для зберігання номеру телефону з валідацією (10 цифр)
class Phone(Field):
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid phone number. Must be 10 digits.")
        super().__init__(value)

    # Валідація формату телефону (10 цифр)
    @staticmethod
    def is_valid(phone):
        return bool(re.match(r"^\d{10}$", phone))

## Клас для зберігання дня народження
class Birthday(Field):
    def __init__(self, value):
        try:
            # Перевірка формату дати: DD.MM.YYYY
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

## Клас для зберігання інформації про контакт (ім'я + телефони)
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None  # Поле день народження може бути порожнім

    # Додавання телефону до контакту
    def add_phone(self, phone):
        self.phones.append(Phone(phone))  # Додаємо телефон у вигляді об'єкта Phone

    # Видалення телефону з контакту
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    # Редагування телефону в контакті
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

    # Пошук телефону в контакті
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    # Додавання дня народження
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday if self.birthday else 'Not set'}"

## Клас для зберігання та управління адресною книгою (словник)
class AddressBook(UserDict):
    # Додавання запису в книгу контактів
    def add_record(self, record):
        self.data[record.name.value] = record

    # Пошук запису за іменем
    def find(self, name):
        return self.data.get(name)

    # Видалення запису з книги за іменем
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    # Отримання списку контактів, чий день народження наступного тижня
    def get_upcoming_birthdays(self):
        today = datetime.today()
        upcoming = []
        
        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value
                # Перевірка, чи вже минув день народження цього року
                birthday_this_year = birthday.replace(year=today.year)

                # Якщо день народження вже минув в цьому році, розглядаємо наступний рік
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                
                # Перевірка, чи день народження в межах наступного тижня
                if today <= birthday_this_year <= today + timedelta(days=7):
                    upcoming.append(record)
        
        return upcoming

# Функція для збереження адресної книги у файл
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

# Функція для завантаження адресної книги з файлу
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Якщо файл не знайдено, повертається новий об'єкт AddressBook

# Декоратор для обробки помилок
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Missing argument. Please check the command format."
    return wrapper

# Функції команд
@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday for {name} added."
    else:
        return f"Contact {name} not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday}"
    elif record:
        return f"{name} does not have a birthday set."
    else:
        return f"Contact {name} not found."

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{record.name.value}: {record.birthday}" for record in upcoming_birthdays])
    return "No upcoming birthdays this week."

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Phone for {name} changed from {old_phone} to {new_phone}."
    return f"Contact {name} not found."

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return f"Phones for {name}: {'; '.join(p.value for p in record.phones)}"
    return f"Contact {name} not found."

@input_error
def show_all_contacts(args, book):
    if book.data:
        return "\n".join([str(record) for record in book.data.values()])
    return "No contacts in the address book."

# Головна функція
def main():
    book = load_data()  # Завантажуємо адресну книгу при запуску
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            save_data(book)  # Зберігаємо адресну книгу при виході
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all_contacts(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

import hashlib
import uuid

class User:
    """
    Базовый класс, представляющий пользователя.
    """
    users = []  # Список для хранения всех пользователей

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.hashed_password = self.hash_password(password)
        self.session_status = None
        User.users.append(self)

    @staticmethod
    def hash_password(password):
        """
        Хеширование пароля с использованием SHA-256.
        """
        b_password = password.encode('utf-8')
        hashed_password = hashlib.sha256(b_password)
        return hashed_password.hexdigest()

    @staticmethod
    def check_password(stored_password, provided_password):
        """
        Проверка пароля.
        """
        b_provided_password = provided_password.encode('utf-8')
        hashed_provided_password = hashlib.sha256(b_provided_password)
        return stored_password == hashed_provided_password.hexdigest()

    def get_details(self):
        """
        Возвращает детали пользователя.
        """
        return f"Пользователь: {self.username}, e-mail: {self.email}"

class Customer(User):
    """
    Класс, представляющий клиента, наследующий класс User.
    """
    def __init__(self, username, email, password, address):
        super().__init__(username, email, password)
        self.address = address

    def get_details(self):
        """
        Возвращает детали клиента.
        """
        return f"{super().get_details()}, Адрес: {self.address}"

class Admin(User):
    """
    Класс, представляющий администратора, наследующий класс User.
    """
    def __init__(self, username, email, password, admin_level):
        super().__init__(username, email, password)
        self.admin_level = admin_level

    def get_details(self):
        """
        Возвращает детали администратора.
        """
        return f"{super().get_details()}, Admin Level: {self.admin_level}"

    @staticmethod
    def list_users():
        """
        Выводит список всех пользователей.
        """
        print("--- Список пользователей: ---")
        for user in User.users:
            print(user.get_details())
        return "--- Конец списка ---"

    @staticmethod
    def delete_user(username):
        """
        Удаляет пользователя по имени пользователя.
        """
        for user in User.users:
            if user.username == username:
                User.users.remove(user)
                print(f"Пользователь {username} удалён")
                return
        print(f"Пользователь {username} не найден")

class AuthenticationService:
    """
    Сервис для управления регистрацией и аутентификацией пользователей.
    """
    def __init__(self):
        self.current_user = None

    def register(self, user_class, username, email, password, *args):
        """
        Регистрация нового пользователя.
        """
        for user in User.users:
            if user.username == username:
                return f"Пользователь с именем {username} уже существует!"
        new_user = user_class(username, email, password, *args)
        return f"Пользователь с именем {username} зарегистрирован"

    def login(self, username, password):
        """
        Аутентификация пользователя.
        """
        for user in User.users:
            if user.username == username and user.check_password(user.hashed_password, password):
                user.session_status = str(uuid.uuid4())
                self.current_user = user
                return f"Аутентификация пользователя {user.username} прошла успепешно"
        return "Некорректное имя пользователя или пароль"

    def logout(self):
        """
        Выход пользователя из системы.
        """
        if self.current_user:
            self.current_user.session_status = None
            self.current_user = None
            return "Выход пользователя прошёл успешно"
        return "Такого пользователя нет в системе"

    def get_current_user(self):
        """
        Возвращает текущего вошедшего пользователя.
        """
        if self.current_user:
            return self.current_user.get_details()
        return "Такого пользователя нет в системе"



# Пример использования

auth_service = AuthenticationService()

print(auth_service.register(Customer, "Дмитрий", "dmitry.romanov.1985@gmail.com", "password123", "Бутлерова 17, 3 этаж"))
print(auth_service.register(Admin, "Михаил", "mikhail.derkunov@neural-university.ru", "admin123", "Super Admin"))
print()

print(Admin.list_users())
print()

print(auth_service.login("Дмитрий", "password123"))
print(auth_service.login("Михаил", "admin123"))
print()

print(auth_service.get_current_user())
print()

print(auth_service.logout())
print()

print(auth_service.get_current_user())
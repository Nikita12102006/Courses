from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm

# Класс для тестирования представления регистрации
class RegisterViewTest(TestCase):
    def setUp(self):
        # Создаем экземпляр клиента для отправки запросов
        self.client = Client()

    # Тестируем загрузку страницы регистрации
    def test_register_page_loads_correctly(self):
        """
        Проверяем, что страница регистрации загружается корректно:
        1. Возвращает HTTP статус 200 (страница найдена).
        2. Используется правильный шаблон 'accounts/register.html'.
        """
        response = self.client.get(reverse('register'))  # Получаем страницу регистрации
        self.assertEqual(response.status_code, 200)  # Проверяем статус ответа
        self.assertTemplateUsed(response, 'accounts/register.html')  # Проверяем шаблон

    # Тестируем успешную регистрацию пользователя
    def test_successful_registration_redirects_to_login(self):
        """
        Проверяем успешную регистрацию пользователя:
        1. Передаем корректные данные в форму регистрации.
        2. Проверяем, что после успешной регистрации идет перенаправление на страницу /login/.
        3. Проверяем, что пользователь создается в базе данных.
        """
        data = {  # Данные для регистрации
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'strongpassword123!',  # Должны соответствовать правилам безопасности
            'password2': 'strongpassword123!'  # Повтор пароля
        }
        response = self.client.post(reverse('register'), data=data)  # Отправляем POST-запрос
        self.assertRedirects(response, '/login/')  # Проверяем, что произошла переадресация
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Проверяем создание пользователя

# Класс для тестирования представления авторизации
class LoginViewTest(TestCase):
    def setUp(self):
        # Готовим клиента и создаем тестового пользователя
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='correctpassword123'
        )  # Создаем пользователя для последующего входа

    # Тестируем загрузку страницы авторизации
    def test_login_page_loads_correctly(self):
        """
        Проверяем, что страница авторизации открывается корректно:
        1. Статус ответа — 200 (страница найдена).
        2. Используется верный шаблон 'accounts/login.html'.
        """
        response = self.client.get(reverse('login'))  # Получаем страницу авторизации
        self.assertEqual(response.status_code, 200)  # Проверяем статус ответа
        self.assertTemplateUsed(response, 'accounts/login.html')  # Проверяем шаблон

    # Тестируем успешную авторизацию пользователя
    def test_successful_login_redirects_homepage(self):
        """
        Проверяем успешную авторизацию пользователя:
        1. Передаем корректные данные в форму авторизации.
        2. Проверяем, что после успешной авторизации идет перенаправление на главную страницу (/).
        3. Проверяем, что пользователь авторизовался (наличие '_auth_user_id' в сессии).
        """
        data = {  # Входные данные
            'username': 'testuser',
            'password': 'correctpassword123'
        }
        response = self.client.post(reverse('login'), data=data)  # Отправляем POST-запрос
        self.assertRedirects(response, '/')  # Проверяем, что произошла переадресация
        self.assertTrue('_auth_user_id' in self.client.session)  # Проверяем авторизацию

# Класс для тестирования представления выхода (logout)
class LogoutViewTest(TestCase):
    def setUp(self):
        # Создаем клиента и принудительно авторизовываемся
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='correctpassword123'
        )
        self.client.force_login(self.user)  # Принудительная авторизация пользователя

    # Тестируем выход пользователя
    def test_logout_redirects_homepage(self):
        """
        Проверяем успешный выход пользователя:
        1. Выполняем GET-запрос на URL выхода.
        2. Проверяем, что произошел редирект на главную страницу.
        3. Проверяем, что пользователь вышел из системы (_auth_user_id удалился из сессии).
        """
        response = self.client.get(reverse('logout'))  # Отправляем запрос на выход
        self.assertRedirects(response, '/')  # Проверяем редирект
        self.assertFalse('_auth_user_id' in self.client.session)  # Проверяем, что пользователь вышел

# Класс для тестирования формы регистрации
class RegistrationFormTest(TestCase):
    def test_valid_form_creates_user(self):
        """
        Проверяем корректную работу формы регистрации:
        1. Передаем валидные данные.
        2. Проверяем, что форма считается действительной.
        3. Сохраняем пользователя и проверяем, что он является экземпляром модели User.
        """
        form_data = {  # Валидные данные
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!'
        }
        form = RegistrationForm(data=form_data)  # Создаем форму с указанными данными
        self.assertTrue(form.is_valid())  # Проверяем, что форма прошла валидацию
        user = form.save()  # Сохраняем пользователя
        self.assertIsInstance(user, User)  # Проверяем, что сохраненный объект — экземпляр User

    def test_invalid_form_rejects_creation(self):
        """
        Проверяем отказ формы при передаче недействительных данных:
        1. Передаем недействительными данные (пропущенное поле username, слабые пароли).
        2. Проверяем, что форма отвергнута.
        3. Проверяем наличие ошибок в форме.
        """
        invalid_data = {  # Недействительные данные
            'username': '',  # Обязательное поле пропускаем
            'email': 'test@example.com',
            'password1': 'WeakPwd',
            'password2': 'DifferentPwd'
        }
        form = RegistrationForm(data=invalid_data)  # Создаем форму с недействительным набором данных
        self.assertFalse(form.is_valid())  # Проверяем, что форма не проходит валидацию
        self.assertGreater(len(form.errors), 0)  # Проверяем, что есть ошибки в форме

# Класс для тестирования формы авторизации
class LoginFormTest(TestCase):
    def setUp(self):
        # Создаем пользователя для последующей авторизации
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='correctpassword123'
        )

    def test_valid_login_data_passes_validation(self):
        """
        Проверяем корректную работу формы авторизации:
        1. Передаем валидные данные (совпадающие с тестовым пользователем).
        2. Проверяем, что форма успешно проходит валидацию.
        """
        valid_data = {  # Действительные данные
            'username': 'testuser',
            'password': 'correctpassword123'
        }
        form = LoginForm(data=valid_data)  # Создаем форму с указанными данными
        self.assertTrue(form.is_valid())  # Проверяем, что форма валидная

    def test_invalid_login_data_fails_validation(self):
        """
        Проверяем отказ формы при передаче недействительных данных:
        1. Передаем неверные данные (несуществующий пользователь или неправильный пароль).
        2. Проверяем, что форма отвергнута.
        """
        invalid_data = {  # Недействительные данные
            'username': 'nonexistentuser',
            'password': 'wrongpassword'
        }
        form = LoginForm(data=invalid_data)  # Создаем форму с недостоверными данными
        self.assertFalse(form.is_valid())  # Проверяем, что форма не валидная
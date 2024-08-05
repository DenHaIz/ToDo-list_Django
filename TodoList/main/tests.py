from django.test import TestCase
from django.urls import reverse


class TestTODO(TestCase):

    """Проверка на работоспособность страницы для входа """
    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    """Проверка на работоспособность страницы для регистрации """
    def test_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
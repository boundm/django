from django.test import TestCase
from .models import Article
from django.utils import timezone

from .forms import ArticleForm

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from django.test import TestCase

class ArticleModelTest(TestCase):
    
    def setUp(self):

        self.article = Article.objects.create(
            title="Тестовая статья",
            content="Содержимое тестовой статьи",
            pub_date=timezone.now()
        )

    def test_article_creation(self):
        """Проверяем, что статья создается правильно"""
        article = self.article
        self.assertEqual(article.title, "Тестовая статья")
        self.assertEqual(article.content, "Содержимое тестовой статьи")
        self.assertIsInstance(article.pub_date, timezone.datetime)
    
    def test_article_string_representation(self):
        """Проверяем строковое представление статьи"""
        article = self.article
        self.assertEqual(str(article), article.title)



class ArticleFormTest(TestCase):

    def test_valid_form(self):
        """Проверяем, что форма корректно валидируется с правильными данными"""
        form_data = {
            'title': 'Тестовая статья',
            'content': 'Тестовое содержимое',
        }
        form = ArticleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Проверяем, что форма не валидируется с некорректными данными"""
        form_data = {
            'title': '', 
            'content': 'Тестовое содержимое',
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)  



class ArticleApiTest(APITestCase):

    def setUp(self):
        # Создаем тестовую статью
        self.article = Article.objects.create(
            title="Тестовая статья",
            content="Содержимое тестовой статьи",
        )
        self.url = reverse('article-list')  

    def test_create_article(self):
        """Тестируем создание статьи через API"""
        data = {
            'title': 'Новая статья',
            'content': 'Содержимое новой статьи',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_article(self):
        """Тестируем получение статьи через API"""
        response = self.client.get(reverse('article-detail', args=[self.article.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.article.title)

    def test_update_article(self):
        """Тестируем обновление статьи через API"""
        data = {'title': 'Обновленная статья', 'content': 'Обновленное содержимое'}
        response = self.client.put(reverse('article-detail', args=[self.article.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Обновленная статья')

    def test_delete_article(self):
        """Тестируем удаление статьи через API"""
        response = self.client.delete(reverse('article-detail', args=[self.article.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())



class ErrorHandlingTest(TestCase):

    def test_page_not_found(self):
        """Тестируем, что несуществующая страница возвращает ошибку 404"""
        response = self.client.get('/some/nonexistent/url/')
        self.assertEqual(response.status_code, 404)

from django.urls import reverse

from django.test import TestCase, Client
from . import models

# class Tests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.news = models.News.objects.create(
#             title = 'Тестовая новость'
#         )
#         self.news_data = {
#             'title': 'Тестовая новость1',
#             'content': 'Lorum Pisum',
#             'category': 1,
#             'is_published': True
#         }
#
#         self.category = models.Category.objects.create(
#             title = 'Тестовая категория'
#         )
#
#     # Тесты страниц
#     def test_index(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_category(self):
#         response = self.client.get(f'/category/{self.category.pk}/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_signin(self):
#         response = self.client.get('/signin/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_redirect(self):
#         response = self.client.get('/youtube/')
#         self.assertEqual(response.status_code, 302)
#
#     def test_categories(self):
#         response = self.client.get('/category/')
#         self.assertEqual(response.status_code, 200)
#
#     # Тесты ModelViewSet
#
#     def test_create(self):
#         response = self.client.post('/news/', self.news_data)
#         self.assertEqual(response.status_code, 201)
#
#     def test_list(self):
#         response = self.client.get('/news/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_detail(self):
#         # response = self.client.get(f'/news/{self.news_data['category']}')
#         # self.assertEqual(response.status_code, 200)
#         url = reverse('news-detail', kwargs={'pk': self.news.pk})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_update(self):
#         url = reverse('news-detail', kwargs={'pk': self.news.pk})
#         put_data = {
#             'title': 'Новость тестовая',
#             'content': 'Ipsum Lorum'
#         }
#         response = self.client.put(url, put_data, content_type='application/json')
#         self.assertEqual(response.status_code, 200)
#
#     def test_partial_update(self):
#         url = reverse('news-detail', kwargs={'pk': self.news.pk})
#         patch_data = {
#             'title': 'Нет рикролам в редиректах!'
#         }
#         response = self.client.put(url, patch_data, content_type='application/json')
#         self.assertEqual(response.status_code, 200)
#         print(self.news.pk)
#
#     def test_delete(self):
#         url = reverse('news-detail', kwargs={'pk': self.news.pk})
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, 204)
import unittest
from django.test import Client, SimpleTestCase
from django.urls import reverse


class MainPageTest(SimpleTestCase):

   def setUp(self):
       self.client = Client()

   def test_index_page(self):
       url = reverse('index')
       response = self.client.get(url)
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, 'main/index.html')
       self.assertTemplateUsed(response, 'main/main.html')
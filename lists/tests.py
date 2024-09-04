from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item


class HomePageTest(TestCase):
    """Тест домашней страницы"""

    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self):
        response = self.client.post("/", data={"item_text": "A new list item"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/lists/only-one/")

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    def test_saving_and_retrieving_items(self):
        first_item = Item.objects.create(text="The first (ever) list item")
        second_item = Item.objects.create(text="Item the second")

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "Item the second")


class ListViewTest(TestCase):
    """тест представления списка"""

    def test_uses_list_template(self):
        response = self.client.get('/lists/only-one/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        """тест - отображаются все элементы списка"""
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")

        response = self.client.get("/lists/only-one/")

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

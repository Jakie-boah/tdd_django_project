from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError


class ListAndItemModelsTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        '''тест: элемент связан со списком'''

        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        """тест: нельзя добавлять пустые элементы списка"""

        list_ = List.objects.create()

        item = Item(list=list_, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        """тест: получен абсолютный url"""

        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}/")

    def test_duplicate_items_are_invalid(self):
        '''тест: повторы элементов не допустимы'''

        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')

        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  #

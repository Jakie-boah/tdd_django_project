from unittest import skip
from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(by=By.CSS_SELECTOR, value='.has-error').text.strip(),
                "You can't have an empty list item")
        )

        # Эдит пробует снова теперь с неким текстом для элемента, и это
        # теперь срабатывает
        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Как ни странно, она решает отправить второй пустой элемент списка
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Эдит получает аналогичное предупреждение на странице списка
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(by=By.CSS_SELECTOR, value='.has-error').text.strip(),
                "You can't have an empty list item"
            )
        )
        # И она может его исправить, заполнив поле неким текстом
        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea'),

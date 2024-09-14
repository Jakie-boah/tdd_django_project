from unittest import skip
from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element(by=By.ID, value='id_new_item').send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(by=By.CSS_SELECTOR, value='.has-error').text,
                "You can't have an empty list item")
        )

        # Эдит пробует снова теперь с неким текстом для элемента, и это
        # теперь срабатывает
        self.browser.find_element(by=By.ID, value='id_new_item').send_keys('Buy milk')
        self.browser.find_element(by=By.ID, value='id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Как ни странно, она решает отправить второй пустой элемент списка
        self.browser.find_element(by=By.ID, value='id_new_item').send_keys(Keys.ENTER)

        # Эдит получает аналогичное предупреждение на странице списка
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                "You can't have an empty list item"
            )
        )
        # И она может его исправить, заполнив поле неким текстом self.browser.find_element_by_id('id_new_item').send_keys('Make tea') self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER) self.wait_for_row_in_list_table('1: Buy milk') self.wait_for_row_in_list_table('2: Make tea'),

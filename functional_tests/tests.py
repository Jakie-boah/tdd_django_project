from selenium import webdriver
import unittest

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
from django.test import LiveServerTestCase

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """Тест нового посетителя"""

    def setUp(self):
        self.browser = webdriver.Safari()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(by=By.ID, value="id_list_table")
                rows = table.find_elements(by=By.TAG_NAME, value="tr")
                self.assertIn(row_text, [row.text.strip() for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e

                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(by=By.TAG_NAME, value="h1").text
        self.assertIn("To-Do", header_text)

        inputbox = self.browser.find_element(by=By.ID, value="id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        inputbox.send_keys("Купить павлиньи перья")

        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Купить павлиньи перья")

        inputbox = self.browser.find_element(by=By.ID, value="id_new_item")
        inputbox.send_keys("Сделать мушку из павлиньих перьев")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Купить павлиньи перья")
        self.wait_for_row_in_list_table("2: Сделать мушку из павлиньих перьев")

        self.fail("закончить тест!")

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(by=By.TAG_NAME, value="h1").text
        self.assertIn("To-Do", header_text)

        inputbox = self.browser.find_element(by=By.ID, value="id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        inputbox.send_keys("Купить павлиньи перья")

        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Купить павлиньи перья")

        inputbox = self.browser.find_element(by=By.ID, value="id_new_item")
        inputbox.send_keys("Сделать мушку из павлиньих перьев")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Купить павлиньи перья")
        self.wait_for_row_in_list_table("2: Сделать мушку из павлиньих перьев")

        self.fail("закончить тест!")

    def test_multiple_users_can_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(by=By.ID, value="id_new_item")
        inputbox.send_keys('Купить павлиньи перья')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Safari()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(by=By.TAG_NAME, value="body").text
        self.assertNotIn('Купить павлиньи перья', page_text.strip())
        self.assertNotIn('Сделать мушку', page_text.strip())

        inputbox = self.browser.find_element(by=By.ID, value="id_new_item")
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        francis_lit_url = self.browser.current_url
        self.assertRegex(francis_lit_url, '/lists/.+')
        self.assertNotEqual(francis_lit_url, edith_list_url)

        page_text = self.browser.find_element(by=By.TAG_NAME, value="body").text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)


if __name__ == "__main__":
    unittest.main(warnings="ignore")

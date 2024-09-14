from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unittest import skip
from .base import FunctionalTest

MAX_WAIT = 5


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Эдит открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # Она замечает, что поле ввода аккуратно центрировано
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512,
            delta=10
        )

        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')

        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512,
            delta=10
        )

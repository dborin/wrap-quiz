#!/usr/bin/env python

import os
import random
from selenium import webdriver
import string
import time
import unittest

class WrapTestCase(unittest.TestCase):
    base_url = os.getenv('WRAP_TEST_BASE_URL', 'x1.wrapdev.net')
    browser_name = os.getenv('WRAP_TEST_BROWSER', 'firefox')
    random_username = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(32))

    def setUp(self):
        if self.browser_name == 'firefox':
            self.driver = webdriver.Firefox()
        elif self.browser_name == 'chrome':
            self.driver = webdriver.Chrome()
        start_url = 'https://www.' + self.base_url + '/index'
        self.driver.get(start_url)

    def test_wrap_site(self):
        driver = self.driver
        random_email = self.random_username + '@example.com'

        driver.find_element_by_link_text('PLANS & PRICING').click()

        # There are 2 identical elements and Selenium barfs with "another element would have gotten the click..." error
        # so grab them all and click on the last one
        signups = driver.find_elements_by_link_text('SIGN UP')
        signups[1].click()

        # Input the randomly generated email address
        email_field = driver.find_element_by_css_selector('input.o-auth-input')
        email_field.send_keys(random_email)
        driver.find_element_by_xpath("//button[@type='submit']").click()

        # Again there are multiple elements that look the same
        time.sleep(3)
        driver.find_element_by_css_selector("div.signup_suggested-username").click()
        for p in driver.find_elements_by_xpath("//input[@type='password']"):
            if p.get_attribute("placeholder") == "Password":
                p.send_keys("password1")
        driver.find_element_by_xpath("//button[@type='submit']").click()

        # Again, no good way to uniquely ID the necessary elements, so forced to
        # find them all and iterate through them, using the placeholder value to
        # find the correct element under test
        for p in driver.find_elements_by_css_selector("input.o-auth-input"):
            if p.get_attribute("placeholder") == "First Name *":
                p.send_keys("John")
            elif p.get_attribute("placeholder") == "Last Name *":
                p.send_keys("Smith")
            elif p.get_attribute("placeholder") == "Company *":
                p.send_keys("Wrap")
            elif p.get_attribute("placeholder") == "Phone Number":
                p.send_keys("212-555-1212")
        driver.find_element_by_xpath("//button[@type='submit']").click()

        # Start creating a wrap
        time.sleep(5)
        driver.find_element_by_css_selector("a.wraps_create-btn").click()
        time.sleep(10)
        templates = driver.find_elements_by_xpath("//button[@type='button']")
        for t in templates:
            if t.get_attribute("ng-click") == "createFromTemplate(template.id)":
                t.click()
                break

        # Wait for the wrap to be created.  30 seconds should be enough time.
        time.sleep(30)
        buttons = driver.find_elements_by_xpath("//button[@type='button']")
        for b in buttons:
            if b.text == "PUBLISH":
                b.click()
                break
        # Wait for the wrap to be published.  Again, 30 seconds should be enough.
        time.sleep(30)

    def tearDown(self):
        self.driver.close()


def suite():
    tests = ['test_wrap_site']
    return unittest.TestSuite(map(WrapTestCase, tests))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

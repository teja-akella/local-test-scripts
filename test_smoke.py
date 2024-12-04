# test_smoke.py

import pytest
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

from utils import setup, login
	
def test_open_copilot(setup):
	driver = setup

	login(setup)
	wait = WebDriverWait(driver, timeout=10)
	open_copilot = wait.until(
		EC.element_to_be_clickable((By.XPATH, "//div[@class='cursor-pointer']"))
	)
	open_copilot.click()

	wait.until(EC.presence_of_element_located((By.XPATH, "//h3[text()='Skills']")))
	time.sleep(5)
	
def test_upload_doc(setup):
	driver = setup
	wait = WebDriverWait(driver, timeout=10)
	upload_file = "/Users/yashdua/Documents/101GenAi_test_docs/Public Beta Launch Test Cases - requirements import structure.pdf"
	time.sleep(5)
	# footer = wait.until(
	# 	EC.presence_of_element_located((By.TAG_NAME, "footer"))
	# )
	# delta_y = footer.rect['y']
	ActionChains(driver).scroll_by_amount(0, 1000).perform()
	# file_button = wait.until(
	# 	EC.element_to_be_clickable((By.XPATH, "//span[text()='Click to browse']"))
	# )
	#file_button.click()
	file_input = driver.find_element(By.XPATH, "(//input[@type='file'])[last()]")
	#time.sleep(1)
	file_input.send_keys(upload_file)
	check_icon = wait.until(
		EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'check-circle')]"))
	)
	time.sleep(5)

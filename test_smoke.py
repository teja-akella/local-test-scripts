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
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from pytest_check import check
from utils import setup, login, open_copilot

def test_create_copilot(setup, name="Test Copilot"):
	driver = setup
	wait = WebDriverWait(driver, timeout=30)
	login(setup)
	main_input = driver.find_element(By.XPATH, "//textarea")
	main_input.send_keys("You are an expert on musculoskeletal (MSK) issues, physiotherapy techniques and yoga exercises, having a conversation with a human patient. Answer their queries about MSK issues and recommend yoga exercises that will help their pain.")
	main_input.send_keys(Keys.ENTER)
	continue_button = wait.until(
		EC.presence_of_element_located((By.XPATH, "//button[@class='text-white py-2 px-4 text-sm font-medium rounded-md bg-pink-dark']"))
	)
	time.sleep(2)
	continue_button.click()
	wait.until(
		EC.presence_of_element_located((By.XPATH, "//h3[text()='What do you want to name your copilot?']"))
	)
	name_prompt = driver.find_element(By.XPATH, "//input[@type='text']")
	name_prompt.send_keys(name)
	avatar = driver.find_element(By.XPATH, "//img[@alt='Copilot Avatar test-image-id-1']")
	avatar.click()
	build_copilot_button = driver.find_element(By.XPATH, "//span[text()='Build Copilot']")
	build_copilot_button.click()
	copilot_name = wait.until(
		EC.presence_of_element_located((By.XPATH, "//h1[text()='Test Copilot']"))
	)
	check.not_equal(copilot_name, None, "Name not found, Copilot not created")

def test_upload_doc(setup):
	driver = setup
	wait = WebDriverWait(driver, timeout=15)
	upload_file = "/var/lib/jenkins/workspace/101GenAi_test_docs/Public Beta Launch Test Cases - requirements import structure.pdf"
	ActionChains(driver).scroll_by_amount(0, 1000).perform()
	file_input = driver.find_element(By.XPATH, "(//input[@type='file'])[last()]")
	file_input.send_keys(upload_file)
	check_icon = wait.until(
		EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'check-circle')]"))
	)
	check.not_equal(check_icon, None, "Successful document upload snackbar did not pop up.")
	try:
		check_icon_kb = wait.until(
			EC.presence_of_element_located((By.XPATH, "//span[text()='Public Beta Launch Test Cases - requirements import structure.pdf']//following::img[@alt='failed icon']"))
		)
		check.equal(check_icon_kb, None, "Failed icon appeared for document upload.")
	except TimeoutException:
		pass
	try:
		check_icon_kb = driver.find_element(By.XPATH, "//span[text()='Public Beta Launch Test Cases - requirements import structure.pdf']//following::img[@alt='completed icon']")
	except NoSuchElementException:
		pass
	check.not_equal(check_icon_kb, None, "Knowledge Base still processing upload of document after ~30seconds.")

def test_upload_url(setup):
	driver = setup
	wait = WebDriverWait(driver, timeout=15)
	url_input = driver.find_element(By.XPATH, "//input[@type='text']")
	url_input.send_keys("https://www.flexifyme.com/")
	time.sleep(3)
	url_submit = driver.find_element(By.XPATH, "//span[text()='Add URL']")
	url_submit.click()
	check_icon_snackbar = wait.until(
		EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'check-circle')]"))
	)
	check.not_equal(check_icon_snackbar, None, "Successful URL upload snackbar did not pop up.")
	try:
		check_icon_kb = wait.until(
			EC.presence_of_element_located((By.XPATH, "//span[text()='Public Beta Launch Test Cases - requirements import structure.pdf']//following::img[@alt='failed icon']"))
		)
		check.equal(check_icon_kb, None, "Failed icon appeared for document upload.")
	except TimeoutException:
		pass
	try:
		check_icon_kb = driver.find_element(By.XPATH, "//span[text()='Public Beta Launch Test Cases - requirements import structure.pdf']//following::img[@alt='completed icon']")
	except NoSuchElementException:
		pass
	check.not_equal(check_icon_kb, None, "Knowledge Base still processing upload of document after ~30seconds.")
	# kb icon check consistently fails, not a test issue
	# TODO: test_delete_url

def test_query_copilot(setup):
	driver = setup
	wait = WebDriverWait(driver, timeout=30)
	copilot_input = driver.find_element(By.XPATH, "//textarea")
	copilot_input.send_keys("Please help me create an MSK exercise routine") # real query
	copilot_input.send_keys(Keys.ENTER)
	time.sleep(10)
	response_elems = driver.find_elements(By.XPATH, "(//div[@class='flex flex-col gap-2'])[last()]/child::*")
	char_count = 0
	for i in response_elems:
		char_count += len(i.text)
	check.greater(char_count, 1000, "Copilot response not long enough.")

def test_delete_copilot(setup):
	driver = setup
	wait = WebDriverWait(driver, timeout=10)

	driver.get("https://test.app.101gen.ai/dashboard")

	#time.sleep(10)
	wait.until(
		EC.presence_of_element_located((By.XPATH, "//div[text()='Test Copilot']/ancestor::div[@class='relative group']/following::button"))
	)
	copilot_button = wait.until(
		EC.presence_of_element_located((By.XPATH, "//div[text()='Test Copilot']/ancestor::div[@class='relative group']/following::button"))
	)
	copilot_button.click()

	delete_button = wait.until(
		EC.presence_of_element_located((By.XPATH, "//div[@class='items-center flex justify-between bg-white w-[68px] shadow absolute left-2 top-2']//button"))
	)
	delete_button.click()

	confirm_button = wait.until(
		EC.presence_of_element_located((By.XPATH, "//span[text()='Yes']"))
	)
	confirm_button.click()

	time.sleep(5)
	try:
		copilot_button = wait.until(
			EC.presence_of_element_located((By.XPATH, "//div[text()='Test Copilot']/ancestor::div[@class='relative group']/following::button"))
		)
		check.fail("Copilot not successfully deleted.")
	except TimeoutException:
		pass

# not in smoke
# test that copilot is using docs uplaoded to knowledge base
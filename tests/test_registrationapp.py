import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()

def get_alert_text(driver):
    alert = Alert(driver)
    text = alert.text
    alert.accept()
    return text

# Test 1: Empty username
def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "pwd").send_keys("Password123")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "Username cannot be empty."

# Test 2: Empty password
def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")
    driver.find_element(By.NAME, "username").send_keys("Teja")
    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "Password cannot be empty."

# Test 3: Short password
def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")
    driver.find_element(By.NAME, "username").send_keys("Teja")
    driver.find_element(By.NAME, "pwd").send_keys("tej")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "Password must be at least 6 characters long."

# Test 4: Valid input
def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")
    driver.find_element(By.NAME, "username").send_keys("Teja")
    driver.find_element(By.NAME, "pwd").send_keys("tej123")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(2)
    current_url = driver.current_url
    assert "/submit" in current_url
    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Hello, Teja! Welcome to the website" in body_text
